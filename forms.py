"""
Flask-WTF forms for Princeton Study Group Finder with Authentication
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, PasswordField, BooleanField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange
from models import User


class RegistrationForm(FlaskForm):
    """Form for user registration"""
    email = StringField(
        'Princeton Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address'),
            Length(max=120)
        ],
        render_kw={'placeholder': 'netid@princeton.edu'}
    )

    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=20, message='Username must be between 3 and 20 characters'),
            Regexp('^[A-Za-z0-9_]+$', message='Username must contain only letters, numbers, and underscores')
        ],
        render_kw={'placeholder': 'e.g., jsmith26'}
    )

    full_name = StringField(
        'Full Name',
        validators=[
            DataRequired(message='Full name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ],
        render_kw={'placeholder': 'John Smith'}
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=8, message='Password must be at least 8 characters')
        ],
        render_kw={'placeholder': 'At least 8 characters'}
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={'placeholder': 'Re-enter password'}
    )

    class_year = SelectField(
        'Class Year',
        choices=[
            (2026, '2026'),
            (2027, '2027'),
            (2028, '2028'),
            (2029, '2029')
        ],
        coerce=int,
        validators=[DataRequired()]
    )

    def validate_email(self, field):
        """Validate that email ends with @princeton.edu and is unique"""
        if not field.data.endswith('@princeton.edu'):
            raise ValidationError('Must be a Princeton email address (@princeton.edu)')

        user = User.query.filter_by(email=field.data.lower()).first()
        if user:
            raise ValidationError('Email already registered. Please log in.')

    def validate_username(self, field):
        """Validate that username is unique"""
        user = User.query.filter_by(username=field.data.lower()).first()
        if user:
            raise ValidationError('Username already taken. Please choose another.')


class LoginForm(FlaskForm):
    """Form for user login"""
    email_or_username = StringField(
        'Email or Username',
        validators=[
            DataRequired(message='Email or username is required')
        ],
        render_kw={'placeholder': 'netid@princeton.edu or username'}
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required')
        ],
        render_kw={'placeholder': 'Your password'}
    )

    remember_me = BooleanField('Remember Me')


class EditProfileForm(FlaskForm):
    """Form for editing user profile"""
    full_name = StringField(
        'Full Name',
        validators=[
            DataRequired(message='Full name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ]
    )

    class_year = SelectField(
        'Class Year',
        choices=[
            (2026, '2026'),
            (2027, '2027'),
            (2028, '2028'),
            (2029, '2029')
        ],
        coerce=int,
        validators=[DataRequired()]
    )

    new_password = PasswordField(
        'New Password (optional)',
        validators=[
            Length(min=8, message='Password must be at least 8 characters if provided')
        ],
        render_kw={'placeholder': 'Leave blank to keep current password'}
    )

    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            EqualTo('new_password', message='Passwords must match')
        ],
        render_kw={'placeholder': 'Re-enter new password'}
    )


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


class JoinStudyGroupForm(FlaskForm):
    """Form for joining a study group (just CSRF protection)"""
    pass


class CreateDiscussionPostForm(FlaskForm):
    """Form for creating a new discussion post"""
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
    content = TextAreaField(
        'Your Reply',
        validators=[
            DataRequired(message='Reply content is required'),
            Length(min=5, max=2000, message='Reply must be between 5 and 2000 characters')
        ],
        render_kw={'placeholder': 'Write your reply...', 'rows': 4}
    )


class VoteForm(FlaskForm):
    """Form for voting on posts and replies"""
    vote_type = IntegerField(
        'Vote Type',
        validators=[
            NumberRange(min=-1, max=1, message='Vote type must be -1, 0, or 1')
        ]
    )
