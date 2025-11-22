# Princeton Study Group Finder 🎓

A modern, full-stack web application built with Flask that helps Princeton University students find and join study groups for their courses. Connect with classmates, ace your courses together, and build a collaborative learning community!

![Princeton Study Groups](https://img.shields.io/badge/Flask-3.0.0-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-green)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC)

## ✨ Features

### Core Functionality
- 📚 **Browse Courses**: View 15+ popular Princeton courses with active study group counts
- 🔍 **Smart Search**: Find courses by code or title with real-time filtering
- 👥 **Create Study Groups**: Host study sessions with customizable details
- 🤝 **Join Groups**: Easy one-click joining with participant management
- 📅 **Time-based Filtering**: View upcoming, past, or all study groups
- 📍 **Location Filtering**: Filter by in-person or virtual sessions
- ⚡ **Real-time Updates**: Live participant counts and capacity tracking
- 🎨 **Modern UI**: Clean, responsive design with Princeton branding

### User Experience
- **Friendly DateTime Formatting**: "Today at 3:00 PM", "Tomorrow at 2:00 PM"
- **Capacity Management**: Visual indicators for full groups
- **Empty States**: Helpful messages when no groups exist
- **Flash Messages**: Clear success/error feedback
- **Form Validation**: Comprehensive client and server-side validation
- **Modal Interactions**: Smooth join experience with modal dialogs

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python 3.x with Flask
- **ORM**: SQLAlchemy for database operations
- **Database**: SQLite (study_groups.db)
- **Templates**: Jinja2 with server-side rendering
- **Forms**: Flask-WTF for form handling and CSRF protection
- **Styling**: Tailwind CSS via CDN
- **Icons**: Heroicons (SVG)

### Project Structure
```
vibe-a-thon_2/
├── app.py                  # Main Flask application with routes
├── models.py               # SQLAlchemy database models
├── forms.py                # Flask-WTF form classes
├── seed_data.py            # Database seeding script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # Jinja2 templates
│   ├── base.html          # Base template with navigation
│   ├── home.html          # Course listing page
│   ├── course_detail.html # Study groups for a course
│   └── create_study_group.html # Create new group form
└── study_groups.db        # SQLite database (created on first run)
```

### Database Schema

**Course**
- `id`: Primary key
- `code`: Unique course code (e.g., "COS126")
- `title`: Course title
- `description`: Course description

**StudyGroup**
- `id`: Primary key
- `course_id`: Foreign key to Course
- `title`: Study group title
- `description`: What the group will cover
- `date_time`: Meeting date and time
- `location`: Meeting location
- `max_participants`: Capacity (-1 for unlimited)
- `host_name`: Name of the host
- `created_at`: Creation timestamp

**Participant**
- `id`: Primary key
- `study_group_id`: Foreign key to StudyGroup
- `name`: Participant name
- `joined_at`: Join timestamp

## 🚀 Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd /Users/neivsinha/Documents/python/vibe-a-thon_2
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and seed the database**
   ```bash
   python seed_data.py
   ```

   This will:
   - Create the SQLite database
   - Add 15 Princeton courses
   - Generate 30+ sample study groups with participants
   - Populate realistic sample data

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: **http://127.0.0.1:5000**
   - You should see the home page with all available courses

## 📖 Usage Guide

### Browsing Courses
1. The home page displays all available courses in a grid layout
2. Each card shows the course code, title, description, and number of active study groups
3. Use the search bar to filter courses by code or title
4. Click any course card to view its study groups

### Viewing Study Groups
1. On a course detail page, you'll see all study groups for that course
2. Use filters to show:
   - **Time**: Upcoming, Past, or All groups
   - **Location**: All, In-Person, or Virtual
3. Each group displays:
   - Title and description
   - Date/time in friendly format
   - Location
   - Host name
   - Current participants / capacity
   - List of all participants

### Creating a Study Group
1. Click "Create Study Group" on any course page
2. Fill out the form:
   - **Title**: e.g., "Midterm Prep Session"
   - **Description**: What you'll cover
   - **Date/Time**: When you'll meet
   - **Location**: Where you'll meet (or "Virtual/Zoom")
   - **Max Participants**: Choose capacity (3-10 or unlimited)
   - **Your Name**: Your name or NetID
3. Click "Create Study Group"
4. You'll be automatically added as the first participant

### Joining a Study Group
1. Find a study group you want to join
2. Click the "Join Group" button
3. Enter your name in the modal
4. Click "Join Group" to confirm
5. You'll see a success message and your name in the participants list

### Additional Features
- **Full Groups**: Groups at capacity show a "FULL" badge and disabled join button
- **Past Groups**: Past study groups are visually dimmed with a "PAST" badge
- **Participant Lists**: See who's already joined each group
- **Responsive Design**: Works great on mobile, tablet, and desktop

## 🎨 Design & Branding

### Princeton Colors
- **Princeton Orange**: `#FF8F00` - Primary accent color
- **Princeton Black**: `#000000` - Primary text and navigation

### Design Philosophy
- Clean, modern aesthetic inspired by university web portals
- Card-based layouts with smooth hover effects
- Consistent spacing and typography
- Mobile-first responsive design
- Intuitive navigation with clear CTAs

## 🔧 Configuration

### Flask Configuration
Located in [app.py](app.py):
- `SECRET_KEY`: Used for session management and CSRF protection
- `SQLALCHEMY_DATABASE_URI`: SQLite database location
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disabled for performance

### Customization
- **Add more courses**: Edit [seed_data.py](seed_data.py) and add to `courses_data`
- **Change colors**: Modify Tailwind config in [templates/base.html](templates/base.html)
- **Add course filters**: Extend filter logic in [app.py](app.py) `course_detail` route

## 📊 Database Management

### Reset Database
To clear and reseed the database:
```bash
python seed_data.py
```

### Manual Database Operations
```python
from app import app
from models import db, Course, StudyGroup, Participant

with app.app_context():
    # Get all courses
    courses = Course.query.all()

    # Get upcoming study groups
    from datetime import datetime
    upcoming = StudyGroup.query.filter(StudyGroup.date_time >= datetime.now()).all()

    # Add a new course
    new_course = Course(code='COS333', title='Advanced Programming', description='...')
    db.session.add(new_course)
    db.session.commit()
```

## 🐛 Troubleshooting

### Database Issues
**Problem**: Database not found or empty
**Solution**: Run `python seed_data.py` to initialize

### Import Errors
**Problem**: `ModuleNotFoundError`
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use
**Problem**: Port 5000 is already in use
**Solution**: Change the port in [app.py](app.py):
```python
app.run(debug=True, port=5001)  # Use a different port
```

### Form Validation Errors
**Problem**: Forms not submitting
**Solution**: Check that:
- Date/time is in the future
- All required fields are filled
- CSRF token is present (automatic with Flask-WTF)

## 🚀 Deployment Considerations

For production deployment, consider:

1. **Database**: Switch from SQLite to PostgreSQL
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
   ```

2. **Secret Key**: Use environment variable
   ```python
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   ```

3. **Debug Mode**: Disable in production
   ```python
   app.run(debug=False)
   ```

4. **WSGI Server**: Use Gunicorn or uWSGI
   ```bash
   gunicorn -w 4 app:app
   ```

5. **Static Assets**: Serve Tailwind locally instead of CDN

## 🤝 Contributing

This is a hackathon project, but improvements are welcome! Areas for enhancement:

- Email notifications for new groups
- User authentication and profiles
- Calendar integration
- Group chat/messaging
- Ratings and reviews
- Mobile app version
- Admin dashboard

## 📝 License

This project is created for educational purposes as part of a hackathon.

## 👥 Team

Built with ❤️ for Princeton University students

## 🎯 Hackathon Demo Tips

1. **Start Fresh**: Run `python seed_data.py` before demo for clean data
2. **Show Workflow**:
   - Browse courses → View study groups → Create new group → Join group
3. **Highlight Features**:
   - Real-time filtering
   - Friendly date formatting
   - Capacity management
   - Responsive design
4. **Mobile Demo**: Show responsive layout on phone
5. **Edge Cases**: Demonstrate full groups, past events, empty states

## 📞 Support

For questions or issues, please check:
- This README
- Code comments in [app.py](app.py), [models.py](models.py), and [forms.py](forms.py)
- Flask documentation: https://flask.palletsprojects.com/

---

**Happy Studying! Go Tigers! 🐅**
