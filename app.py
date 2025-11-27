"""
TigerStudy - Main Flask Application
A modern web app for Princeton students to find and join study groups
"""
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from models import db, bcrypt, User, Course, StudyGroup, Participant, DiscussionPost, DiscussionReply, PostVote, ReplyVote, ChatMessage
from forms import (CreateStudyGroupForm, JoinStudyGroupForm, CreateDiscussionPostForm,
                   CreateDiscussionReplyForm, RegistrationForm, LoginForm, EditProfileForm, VoteForm, ChatMessageForm)
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'tigerstudy-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_groups.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize Bcrypt
bcrypt.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


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


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    # Redirect if already logged in
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Create new user
        user = User(
            email=form.email.data.lower(),
            username=form.username.data,
            full_name=form.full_name.data,
            class_year=form.class_year.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f'Welcome to TigerStudy, {user.full_name}! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    # Redirect if already logged in
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        # Find user by email or username
        email_or_username = form.email_or_username.data.lower()
        user = User.query.filter(
            db.or_(
                User.email == email_or_username,
                User.username == email_or_username
            )
        ).first()

        # Check credentials
        if user and user.check_password(form.password.data):
            # Update last login
            user.last_login = datetime.now()
            db.session.commit()

            # Log user in
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.username}!', 'success')

            # Redirect to next page or home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid email/username or password. Please try again.', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Log out the current user"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    """View current user's profile"""
    # Get user's activity
    hosted_groups = current_user.get_study_groups_hosting()
    joined_groups = current_user.get_study_groups_joined()
    discussion_posts = current_user.get_discussion_posts_created()
    replies_count = current_user.total_replies_count()

    return render_template(
        'profile.html',
        user=current_user,
        hosted_groups=hosted_groups,
        joined_groups=joined_groups,
        discussion_posts=discussion_posts,
        replies_count=replies_count
    )


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit current user's profile"""
    form = EditProfileForm()

    if form.validate_on_submit():
        # Update profile information
        current_user.full_name = form.full_name.data
        current_user.class_year = form.class_year.data

        # Update password if provided
        if form.new_password.data:
            current_user.set_password(form.new_password.data)

        db.session.commit()

        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('profile'))

    # Pre-populate form with current data
    if request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.class_year.data = current_user.class_year

    return render_template('edit_profile.html', form=form)


@app.route('/user/<username>')
def user_profile(username):
    """View another user's public profile"""
    user = User.query.filter_by(username=username).first_or_404()

    # Get user's activity
    hosted_groups = user.get_study_groups_hosting()
    joined_groups = user.get_study_groups_joined()
    discussion_posts = user.get_discussion_posts_created()
    replies_count = user.total_replies_count()

    return render_template(
        'user_profile.html',
        user=user,
        hosted_groups=hosted_groups,
        joined_groups=joined_groups,
        discussion_posts=discussion_posts,
        replies_count=replies_count
    )


# ==================== COURSE AND STUDY GROUP ROUTES ====================

@app.route('/course/<course_code>')
def course_detail(course_code):
    """Course detail page showing all study groups"""
    course = Course.query.filter_by(code=course_code.upper()).first_or_404()

    # Create form for joining groups
    form = JoinStudyGroupForm()

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
        form=form,
        time_filter=time_filter,
        location_type=location_type
    )


@app.route('/course/<course_code>/create', methods=['GET', 'POST'])
@login_required
def create_study_group(course_code):
    """Create a new study group"""
    course = Course.query.filter_by(code=course_code.upper()).first_or_404()
    form = CreateStudyGroupForm()

    if form.validate_on_submit():
        # Check if date is in the future
        if form.date_time.data < datetime.now():
            flash('Study group date must be in the future.', 'error')
            return render_template('create_study_group.html', course=course, form=form)

        # Create new study group with current user as host
        study_group = StudyGroup(
            course_id=course.id,
            host_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            date_time=form.date_time.data,
            location=form.location.data,
            max_participants=form.max_participants.data
        )

        db.session.add(study_group)

        # Automatically add host as first participant
        host_participant = Participant(
            study_group=study_group,
            user_id=current_user.id
        )
        db.session.add(host_participant)

        db.session.commit()

        flash(f'Study group "{study_group.title}" created successfully!', 'success')
        return redirect(url_for('course_detail', course_code=course.code))

    return render_template('create_study_group.html', course=course, form=form)


@app.route('/study_group/<int:group_id>/join', methods=['POST'])
@login_required
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
            # Check if user already joined (using user_id instead of name)
            if study_group.user_is_participant(current_user.id):
                flash('You have already joined this study group.', 'warning')
            else:
                # Add participant
                participant = Participant(
                    study_group_id=group_id,
                    user_id=current_user.id
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


@app.route('/study_group/<int:group_id>/leave', methods=['POST'])
@login_required
def leave_study_group(group_id):
    """Leave a study group"""
    study_group = StudyGroup.query.get_or_404(group_id)
    form = JoinStudyGroupForm()

    if form.validate_on_submit():
        # Check if study group is in the past
        if study_group.is_past():
            flash('Cannot leave a study group that has already occurred.', 'error')
        # Check if user is the host
        elif study_group.host_id == current_user.id:
            flash('You cannot leave a study group you are hosting. Please delete the group instead.', 'warning')
        else:
            # Check if user is actually a participant
            if not study_group.user_is_participant(current_user.id):
                flash('You are not a member of this study group.', 'warning')
            else:
                # Remove participant
                participant = Participant.query.filter_by(
                    study_group_id=group_id,
                    user_id=current_user.id
                ).first()

                if participant:
                    db.session.delete(participant)
                    db.session.commit()
                    flash(f'You have left "{study_group.title}".', 'success')
                else:
                    flash('Error leaving study group.', 'error')
    else:
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'error')

    return redirect(url_for('course_detail', course_code=study_group.course.code))


@app.route('/course/<course_code>/discussions')
def discussion_board(course_code):
    """Discussion board for a course"""
    course = Course.query.filter_by(code=course_code.upper()).first_or_404()

    # Get sort parameter (default: hot)
    sort_by = request.args.get('sort', 'hot')

    # Base query
    query = DiscussionPost.query.filter_by(course_id=course.id)

    # Apply sorting
    if sort_by == 'top':
        # Sort by score (highest first), then by creation time
        posts = query.order_by(
            DiscussionPost.pinned.desc(),
            DiscussionPost.score.desc(),
            DiscussionPost.created_at.desc()
        ).all()
    elif sort_by == 'new':
        # Sort by most recent
        posts = query.order_by(
            DiscussionPost.pinned.desc(),
            DiscussionPost.created_at.desc()
        ).all()
    elif sort_by == 'trending':
        # Posts from last 48 hours sorted by score
        cutoff_time = datetime.now() - timedelta(hours=48)
        posts = query.filter(DiscussionPost.created_at >= cutoff_time).order_by(
            DiscussionPost.pinned.desc(),
            DiscussionPost.score.desc()
        ).all()
    else:  # hot (default)
        # Calculate hot score for each post and sort
        all_posts = query.all()
        # Sort by pinned first, then by hot score
        posts = sorted(all_posts, key=lambda p: (not p.pinned, -p.calculate_hot_score()))

    # Create vote form
    vote_form = VoteForm()

    return render_template('discussion_board.html', course=course, posts=posts, sort_by=sort_by, vote_form=vote_form)


@app.route('/course/<course_code>/discussions/new', methods=['GET', 'POST'])
@login_required
def create_discussion(course_code):
    """Create a new discussion post"""
    course = Course.query.filter_by(code=course_code.upper()).first_or_404()
    form = CreateDiscussionPostForm()

    if form.validate_on_submit():
        # Create new discussion post with current user as author
        post = DiscussionPost(
            course_id=course.id,
            author_id=current_user.id,
            title=form.title.data,
            content=form.content.data,
            category=form.category.data
        )

        db.session.add(post)
        db.session.commit()

        flash(f'Discussion post "{post.title}" created successfully!', 'success')
        return redirect(url_for('discussion_post_detail', post_id=post.id))

    return render_template('create_discussion.html', course=course, form=form)


@app.route('/discussion/<int:post_id>')
def discussion_post_detail(post_id):
    """View individual discussion post with replies"""
    post = DiscussionPost.query.get_or_404(post_id)
    form = CreateDiscussionReplyForm()

    # Get all replies sorted by score (highest first), then by creation time
    replies = DiscussionReply.query.filter_by(post_id=post_id).order_by(
        DiscussionReply.score.desc(),
        DiscussionReply.created_at.asc()
    ).all()

    # Create vote form
    vote_form = VoteForm()

    return render_template('discussion_post_detail.html', post=post, replies=replies, form=form, vote_form=vote_form)


@app.route('/discussion/<int:post_id>/reply', methods=['POST'])
@login_required
def reply_to_discussion(post_id):
    """Add a reply to a discussion post"""
    post = DiscussionPost.query.get_or_404(post_id)
    form = CreateDiscussionReplyForm()

    if form.validate_on_submit():
        # Create new reply with current user as author
        reply = DiscussionReply(
            post_id=post_id,
            author_id=current_user.id,
            content=form.content.data
        )

        db.session.add(reply)
        db.session.commit()

        flash('Reply posted successfully!', 'success')
    else:
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'error')

    return redirect(url_for('discussion_post_detail', post_id=post_id))


@app.route('/discussion/post/<int:post_id>/vote', methods=['POST'])
@login_required
def vote_on_post(post_id):
    """Upvote or downvote a discussion post"""
    post = DiscussionPost.query.get_or_404(post_id)
    form = VoteForm()

    # Check if user is trying to vote on their own post
    if post.author_id == current_user.id:
        flash('You cannot vote on your own post.', 'warning')
        return redirect(request.referrer or url_for('discussion_post_detail', post_id=post_id))

    if form.validate_on_submit():
        vote_type = int(form.vote_type.data)  # Ensure it's an integer

        # Check if user has already voted
        existing_vote = PostVote.query.filter_by(post_id=post_id, user_id=current_user.id).first()

        if vote_type == 0:  # Remove vote
            if existing_vote:
                db.session.delete(existing_vote)
                db.session.commit()
                # Recalculate score
                post.score = sum(v.vote_type for v in post.votes)
                db.session.commit()
        elif existing_vote:
            # Update existing vote if different
            if existing_vote.vote_type != vote_type:
                existing_vote.vote_type = vote_type
                db.session.commit()
                # Recalculate score
                post.score = sum(v.vote_type for v in post.votes)
                db.session.commit()
        else:
            # Create new vote
            new_vote = PostVote(
                post_id=post_id,
                user_id=current_user.id,
                vote_type=vote_type
            )
            db.session.add(new_vote)
            db.session.commit()
            # Recalculate score
            post.score = sum(v.vote_type for v in post.votes)
            db.session.commit()

    return redirect(request.referrer or url_for('discussion_post_detail', post_id=post_id))


@app.route('/discussion/reply/<int:reply_id>/vote', methods=['POST'])
@login_required
def vote_on_reply(reply_id):
    """Upvote or downvote a discussion reply"""
    reply = DiscussionReply.query.get_or_404(reply_id)
    form = VoteForm()

    # Check if user is trying to vote on their own reply
    if reply.author_id == current_user.id:
        flash('You cannot vote on your own reply.', 'warning')
        return redirect(request.referrer or url_for('discussion_post_detail', post_id=reply.post_id))

    if form.validate_on_submit():
        vote_type = int(form.vote_type.data)  # Ensure it's an integer

        # Check if user has already voted
        existing_vote = ReplyVote.query.filter_by(reply_id=reply_id, user_id=current_user.id).first()

        if vote_type == 0:  # Remove vote
            if existing_vote:
                db.session.delete(existing_vote)
                db.session.commit()
                # Recalculate score
                reply.score = sum(v.vote_type for v in reply.votes)
                db.session.commit()
        elif existing_vote:
            # Update existing vote if different
            if existing_vote.vote_type != vote_type:
                existing_vote.vote_type = vote_type
                db.session.commit()
                # Recalculate score
                reply.score = sum(v.vote_type for v in reply.votes)
                db.session.commit()
        else:
            # Create new vote
            new_vote = ReplyVote(
                reply_id=reply_id,
                user_id=current_user.id,
                vote_type=vote_type
            )
            db.session.add(new_vote)
            db.session.commit()
            # Recalculate score
            reply.score = sum(v.vote_type for v in reply.votes)
            db.session.commit()

    return redirect(request.referrer or url_for('discussion_post_detail', post_id=reply.post_id))


# ==================== STUDY GROUP CHAT ROUTES ====================

@app.route('/study_group/<int:group_id>')
@login_required
def study_group_chat(group_id):
    """View study group chat page"""
    group = StudyGroup.query.get_or_404(group_id)

    # Check if user is a participant or host
    if not group.user_is_participant(current_user.id):
        flash('You must be a member of this study group to view the chat.', 'warning')
        return redirect(url_for('course_detail', course_code=group.course.code))

    # Get all chat messages, ordered by pinned first, then by time
    messages = ChatMessage.query.filter_by(study_group_id=group_id).order_by(
        ChatMessage.pinned.desc(),
        ChatMessage.created_at.asc()
    ).all()

    form = ChatMessageForm()

    return render_template('study_group_chat.html',
                         group=group,
                         messages=messages,
                         form=form)


@app.route('/study_group/<int:group_id>/message', methods=['POST'])
@login_required
def send_chat_message(group_id):
    """Send a chat message in a study group"""
    group = StudyGroup.query.get_or_404(group_id)

    # Check if user is a participant or host
    if not group.user_is_participant(current_user.id):
        flash('You must be a member of this study group to send messages.', 'warning')
        return redirect(url_for('course_detail', course_code=group.course.code))

    form = ChatMessageForm()

    if form.validate_on_submit():
        message = ChatMessage(
            study_group_id=group_id,
            author_id=current_user.id,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent!', 'success')

    return redirect(url_for('study_group_chat', group_id=group_id))


@app.route('/study_group/<int:group_id>/message/<int:message_id>/pin', methods=['POST'])
@login_required
def pin_chat_message(group_id, message_id):
    """Pin or unpin a chat message (host only)"""
    group = StudyGroup.query.get_or_404(group_id)
    message = ChatMessage.query.get_or_404(message_id)

    # Check if user is the host
    if group.host_id != current_user.id:
        flash('Only the group host can pin messages.', 'error')
        return redirect(url_for('study_group_chat', group_id=group_id))

    # Check if message belongs to this group
    if message.study_group_id != group_id:
        flash('Invalid message.', 'error')
        return redirect(url_for('study_group_chat', group_id=group_id))

    # Toggle pin status
    message.pinned = not message.pinned
    db.session.commit()

    if message.pinned:
        flash('Message pinned successfully!', 'success')
    else:
        flash('Message unpinned.', 'info')

    return redirect(url_for('study_group_chat', group_id=group_id))


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
    print("TigerStudy")
    print("="*60)
    print("Starting development server...")
    print("Access the app at: http://127.0.0.1:5001")
    print("="*60 + "\n")

    app.run(debug=True, port=5001)
