"""
Princeton Study Group Finder - Main Flask Application
A modern web app for Princeton students to find and join study groups
"""
from flask import Flask, render_template, redirect, url_for, flash, request
from datetime import datetime, timedelta
from models import db, Course, StudyGroup, Participant
from forms import CreateStudyGroupForm, JoinStudyGroupForm
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'princeton-study-groups-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_groups.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)


# Custom Jinja2 filters
@app.template_filter('format_datetime')
def format_datetime(dt):
    """Format datetime in a friendly way"""
    if not dt:
        return ''

    now = datetime.now()
    today = now.date()
    tomorrow = (now + timedelta(days=1)).date()

    if dt.date() == today:
        return f"Today at {dt.strftime('%I:%M %p')}"
    elif dt.date() == tomorrow:
        return f"Tomorrow at {dt.strftime('%I:%M %p')}"
    elif dt.date() < today + timedelta(days=7):
        return dt.strftime('%a, %b %d at %I:%M %p')
    else:
        return dt.strftime('%b %d, %Y at %I:%M %p')


@app.route('/')
def home():
    """Home page showing all courses"""
    search_query = request.args.get('search', '').strip()

    if search_query:
        # Search courses by code or title
        courses = Course.query.filter(
            db.or_(
                Course.code.ilike(f'%{search_query}%'),
                Course.title.ilike(f'%{search_query}%')
            )
        ).order_by(Course.code).all()
    else:
        courses = Course.query.order_by(Course.code).all()

    return render_template('home.html', courses=courses, search_query=search_query)


@app.route('/course/<course_code>')
def course_detail(course_code):
    """Course detail page showing all study groups"""
    course = Course.query.filter_by(code=course_code.upper()).first_or_404()

    # Get filter parameters
    time_filter = request.args.get('time', 'upcoming')
    location_type = request.args.get('location', 'all')

    # Base query
    query = StudyGroup.query.filter_by(course_id=course.id)

    # Apply time filter
    now = datetime.now()
    if time_filter == 'upcoming':
        query = query.filter(StudyGroup.date_time >= now)
    elif time_filter == 'past':
        query = query.filter(StudyGroup.date_time < now)

    # Apply location filter
    if location_type == 'in-person':
        query = query.filter(~StudyGroup.location.ilike('%virtual%'), ~StudyGroup.location.ilike('%zoom%'))
    elif location_type == 'virtual':
        query = query.filter(db.or_(StudyGroup.location.ilike('%virtual%'), StudyGroup.location.ilike('%zoom%')))

    # Order by date/time
    if time_filter == 'past':
        study_groups = query.order_by(StudyGroup.date_time.desc()).all()
    else:
        study_groups = query.order_by(StudyGroup.date_time.asc()).all()

    return render_template(
        'course_detail.html',
        course=course,
        study_groups=study_groups,
        time_filter=time_filter,
        location_type=location_type
    )


@app.route('/course/<course_code>/create', methods=['GET', 'POST'])
def create_study_group(course_code):
    """Create a new study group"""
    course = Course.query.filter_by(code=course_code.upper()).first_or_404()
    form = CreateStudyGroupForm()

    if form.validate_on_submit():
        # Check if date is in the future
        if form.date_time.data < datetime.now():
            flash('Study group date must be in the future.', 'error')
            return render_template('create_study_group.html', course=course, form=form)

        # Create new study group
        study_group = StudyGroup(
            course_id=course.id,
            title=form.title.data,
            description=form.description.data,
            date_time=form.date_time.data,
            location=form.location.data,
            max_participants=form.max_participants.data,
            host_name=form.host_name.data
        )

        db.session.add(study_group)

        # Automatically add host as first participant
        host_participant = Participant(
            study_group=study_group,
            name=form.host_name.data
        )
        db.session.add(host_participant)

        db.session.commit()

        flash(f'Study group "{study_group.title}" created successfully!', 'success')
        return redirect(url_for('course_detail', course_code=course.code))

    return render_template('create_study_group.html', course=course, form=form)


@app.route('/study_group/<int:group_id>/join', methods=['POST'])
def join_study_group(group_id):
    """Join a study group"""
    study_group = StudyGroup.query.get_or_404(group_id)
    form = JoinStudyGroupForm()

    if form.validate_on_submit():
        # Check if group is full
        if study_group.is_full():
            flash('Sorry, this study group is already full.', 'error')
        # Check if study group is in the past
        elif study_group.is_past():
            flash('Cannot join a study group that has already occurred.', 'error')
        else:
            # Check if user already joined
            existing = Participant.query.filter_by(
                study_group_id=group_id,
                name=form.name.data
            ).first()

            if existing:
                flash('You have already joined this study group.', 'warning')
            else:
                # Add participant
                participant = Participant(
                    study_group_id=group_id,
                    name=form.name.data
                )
                db.session.add(participant)
                db.session.commit()

                flash(f'Successfully joined "{study_group.title}"!', 'success')
    else:
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'error')

    return redirect(url_for('course_detail', course_code=study_group.course.code))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    flash('The page you are looking for does not exist.', 'error')
    return redirect(url_for('home'))


@app.context_processor
def utility_processor():
    """Add utility functions to all templates"""
    return dict(now=datetime.now)


if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        print("Database initialized successfully!")

    print("\n" + "="*60)
    print("Princeton Study Group Finder")
    print("="*60)
    print("Starting development server...")
    print("Access the app at: http://127.0.0.1:5001")
    print("="*60 + "\n")

    app.run(debug=True, port=5001)
