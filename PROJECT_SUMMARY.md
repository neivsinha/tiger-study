# Princeton Study Group Finder - Project Summary

## Overview
A full-stack web application built with Flask for Princeton University students to find and join study groups for their courses.

## Project Structure
```
vibe-a-thon_2/
├── app.py                      # Main Flask application (routes, logic)
├── models.py                   # SQLAlchemy database models
├── forms.py                    # Flask-WTF form classes
├── seed_data.py               # Database seeding script
├── requirements.txt           # Python dependencies
├── setup.sh                   # Automated setup script
├── run.sh                     # Quick start script
├── .gitignore                 # Git ignore file
├── README.md                  # Comprehensive documentation
├── PROJECT_SUMMARY.md         # This file
├── templates/                 # Jinja2 HTML templates
│   ├── base.html             # Base template with navigation
│   ├── home.html             # Course grid page
│   ├── course_detail.html    # Study groups listing
│   └── create_study_group.html # Create group form
└── study_groups.db           # SQLite database (created after setup)
```

## Key Features Implemented

### 1. Home Page (/)
- Grid layout of 15 Princeton courses
- Real-time search/filter functionality
- Active study group counts per course
- Princeton orange and black branding
- Responsive card design with hover effects

### 2. Course Detail Page (/course/<code>)
- All study groups for a specific course
- Filter by time: Upcoming, Past, All
- Filter by location: All, In-Person, Virtual
- Display participant lists
- Join functionality with modal
- Empty state messaging
- Visual indicators for full/past groups

### 3. Create Study Group (/course/<code>/create)
- Comprehensive form with validation
- Fields: title, description, datetime, location, capacity, host name
- Client and server-side validation
- Helpful tips section
- Auto-adds host as first participant

### 4. Join Study Group (POST /study_group/<id>/join)
- Modal-based join experience
- Capacity checking
- Duplicate prevention
- Flash message feedback

## Database Schema

### Course
- id (PK)
- code (unique)
- title
- description

### StudyGroup
- id (PK)
- course_id (FK)
- title
- description
- date_time
- location
- max_participants (-1 = unlimited)
- host_name
- created_at

### Participant
- id (PK)
- study_group_id (FK)
- name
- joined_at

## Technology Stack

- **Backend**: Flask 3.0.0
- **ORM**: SQLAlchemy 2.0.44
- **Forms**: Flask-WTF 1.2.1, WTForms 3.1.1
- **Database**: SQLite
- **Frontend**: Jinja2 templates
- **Styling**: Tailwind CSS (via CDN)
- **Icons**: Heroicons (inline SVG)

## Quick Start

### Option 1: Automated Setup
```bash
./setup.sh    # Installs dependencies and seeds database
./run.sh      # Starts the application
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_data.py

# Run application
python app.py
```

Access at: http://127.0.0.1:5000

## Sample Data
The seed script populates:
- 15 Princeton courses (COS126, COS226, MAT201, etc.)
- 37 study groups across all courses
- Realistic participant data
- Mix of upcoming and past meetings
- Various locations (Fine Hall, Frist, Virtual, etc.)

## Design Highlights

### Princeton Branding
- **Primary Color**: Princeton Orange (#FF8F00)
- **Secondary Color**: Princeton Black (#000000)
- Clean, modern university portal aesthetic

### UX Features
- Friendly datetime formatting ("Today at 3:00 PM")
- Visual capacity indicators
- Smooth hover transitions
- Flash message animations
- Modal interactions
- Mobile-responsive layout
- Empty state handling

## Routes Summary

| Route | Method | Description |
|-------|--------|-------------|
| / | GET | Home page with all courses |
| /course/<code> | GET | Study groups for a course |
| /course/<code>/create | GET | Create group form |
| /course/<code>/create | POST | Handle group creation |
| /study_group/<id>/join | POST | Join a study group |

## Key Code Files

### [app.py](app.py) - Main Application
- Flask app configuration
- All route handlers
- Custom Jinja2 filters (datetime formatting)
- Error handling
- Flash message management

### [models.py](models.py) - Database Models
- SQLAlchemy model definitions
- Relationships and foreign keys
- Helper methods (is_full, is_past, etc.)
- Capacity calculations

### [forms.py](forms.py) - Forms
- CreateStudyGroupForm with validation
- JoinStudyGroupForm
- Custom validators
- Field configurations

### [seed_data.py](seed_data.py) - Data Seeding
- Database initialization
- Course data generation
- Study group templates by course
- Random participant assignment

## Notable Implementation Details

1. **Datetime Handling**: Custom Jinja2 filter converts dates to friendly format
2. **Capacity Management**: Supports unlimited (-1) or specific limits
3. **CSRF Protection**: Flask-WTF provides automatic CSRF tokens
4. **Modal Join**: JavaScript-powered modal for smooth UX
5. **Query Filtering**: SQLAlchemy filters for time/location
6. **Host Auto-join**: Host automatically added as first participant
7. **Empty States**: Contextual messaging when no groups exist

## Testing the Application

### Test Workflow
1. Browse courses on home page
2. Use search to filter (try "COS" or "MAT")
3. Click a course to view study groups
4. Use time/location filters
5. Create a new study group
6. Join an existing group
7. Verify participant lists update

### Edge Cases Tested
- Full groups (disabled join button)
- Past groups (visual dimming)
- Empty course (helpful message)
- Form validation (try invalid dates)
- Duplicate joins (prevented)

## Future Enhancements

Potential features for v2:
- User authentication (NetID integration)
- Email notifications
- Calendar integration (.ics export)
- Group chat functionality
- Ratings/reviews
- Admin dashboard
- Mobile app
- Real-time updates (WebSocket)
- Advanced search filters
- Course recommendations

## Performance Considerations

- SQLite suitable for hackathon/demo
- For production: migrate to PostgreSQL
- Add database indexing on frequently queried fields
- Consider caching for course list
- Implement pagination for large group lists

## Security Features

- CSRF protection via Flask-WTF
- SQL injection prevention via SQLAlchemy ORM
- Input validation on all forms
- XSS prevention via Jinja2 auto-escaping
- Secret key for session security

## Browser Compatibility

Tested and working on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Deployment Readiness

For production deployment:
1. Set SECRET_KEY via environment variable
2. Switch to PostgreSQL database
3. Disable debug mode
4. Use production WSGI server (Gunicorn)
5. Serve static assets efficiently
6. Set up proper logging
7. Configure HTTPS
8. Add monitoring/analytics

## License
Educational/Hackathon project for Princeton University

## Credits
Built with Flask, SQLAlchemy, Tailwind CSS, and ❤️

---

**Status**: ✅ Complete and ready for demo
**Last Updated**: 2024
**Version**: 1.0.0
