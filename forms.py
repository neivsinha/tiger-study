"""
Flask-WTF forms for Princeton Study Group Finder
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class CreateStudyGroupForm(FlaskForm):
    """Form for creating a new study group"""
    title = StringField(
        'Study Group Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(min=3, max=200, message='Title must be between 3 and 200 characters')
        ],
        render_kw={'placeholder': 'e.g., Midterm Prep Session'}
    )

    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(message='Description is required'),
            Length(min=10, max=1000, message='Description must be between 10 and 1000 characters')
        ],
        render_kw={'placeholder': 'Describe what you\'ll cover in this study session...', 'rows': 4}
    )

    date_time = DateTimeLocalField(
        'Date and Time',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired(message='Date and time are required')],
        render_kw={'placeholder': 'Select date and time'}
    )

    location = StringField(
        'Location',
        validators=[
            DataRequired(message='Location is required'),
            Length(min=3, max=200, message='Location must be between 3 and 200 characters')
        ],
        render_kw={'placeholder': 'e.g., Frist Campus Center, Room 302'}
    )

    max_participants = SelectField(
        'Max Participants',
        choices=[
            (3, '3 people'),
            (4, '4 people'),
            (5, '5 people'),
            (6, '6 people'),
            (8, '8 people'),
            (10, '10 people'),
            (-1, 'Unlimited')
        ],
        coerce=int,
        validators=[DataRequired()]
    )

    host_name = StringField(
        'Your Name',
        validators=[
            DataRequired(message='Your name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ],
        render_kw={'placeholder': 'Your name or NetID'}
    )


class JoinStudyGroupForm(FlaskForm):
    """Form for joining a study group"""
    name = StringField(
        'Your Name',
        validators=[
            DataRequired(message='Your name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ],
        render_kw={'placeholder': 'Your name or NetID'}
    )


class CreateDiscussionPostForm(FlaskForm):
    """Form for creating a new discussion post"""
    author_name = StringField(
        'Your Name',
        validators=[
            DataRequired(message='Your name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ],
        render_kw={'placeholder': 'Your name or NetID'}
    )

    title = StringField(
        'Post Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(min=5, max=200, message='Title must be between 5 and 200 characters')
        ],
        render_kw={'placeholder': 'e.g., Question about Problem Set 3'}
    )

    category = SelectField(
        'Category',
        choices=[
            ('Question', 'Question'),
            ('Study Tips', 'Study Tips'),
            ('Resources', 'Resources'),
            ('Exam Prep', 'Exam Prep'),
            ('General', 'General')
        ],
        validators=[DataRequired()]
    )

    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(message='Content is required'),
            Length(min=10, max=5000, message='Content must be between 10 and 5000 characters')
        ],
        render_kw={'placeholder': 'Share your question, tip, or resource...', 'rows': 8}
    )


class CreateDiscussionReplyForm(FlaskForm):
    """Form for replying to a discussion post"""
    author_name = StringField(
        'Your Name',
        validators=[
            DataRequired(message='Your name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ],
        render_kw={'placeholder': 'Your name or NetID'}
    )

    content = TextAreaField(
        'Your Reply',
        validators=[
            DataRequired(message='Reply content is required'),
            Length(min=5, max=2000, message='Reply must be between 5 and 2000 characters')
        ],
        render_kw={'placeholder': 'Write your reply...', 'rows': 4}
    )
