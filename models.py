"""
Database models for Princeton Study Group Finder
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Course(db.Model):
    """Model for Princeton courses"""
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Relationships
    study_groups = db.relationship('StudyGroup', backref='course', lazy=True, cascade='all, delete-orphan')
    discussion_posts = db.relationship('DiscussionPost', backref='course', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Course {self.code}: {self.title}>'

    def active_study_groups_count(self):
        """Count active (future) study groups for this course"""
        return StudyGroup.query.filter(
            StudyGroup.course_id == self.id,
            StudyGroup.date_time >= datetime.now()
        ).count()

    def discussion_posts_count(self):
        """Count total discussion posts for this course"""
        return DiscussionPost.query.filter(
            DiscussionPost.course_id == self.id
        ).count()


class StudyGroup(db.Model):
    """Model for study group meetings"""
    __tablename__ = 'study_groups'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)  # -1 for unlimited
    host_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship to participants
    participants = db.relationship('Participant', backref='study_group', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<StudyGroup {self.title}>'

    def is_full(self):
        """Check if the study group is at capacity"""
        if self.max_participants == -1:  # Unlimited
            return False
        return len(self.participants) >= self.max_participants

    def participant_count(self):
        """Get current number of participants"""
        return len(self.participants)

    def is_past(self):
        """Check if the study group date has passed"""
        return self.date_time < datetime.now()

    def formatted_capacity(self):
        """Return formatted capacity string"""
        if self.max_participants == -1:
            return f"{self.participant_count()} participants"
        return f"{self.participant_count()}/{self.max_participants}"


class Participant(db.Model):
    """Model for study group participants"""
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    study_group_id = db.Column(db.Integer, db.ForeignKey('study_groups.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Participant {self.name}>'


class DiscussionPost(db.Model):
    """Model for course discussion posts"""
    __tablename__ = 'discussion_posts'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='General')
    pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship to replies
    replies = db.relationship('DiscussionReply', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<DiscussionPost {self.title}>'

    def reply_count(self):
        """Get number of replies"""
        return len(self.replies)

    def preview_content(self, length=150):
        """Return preview of content"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + '...'

    def time_ago(self):
        """Return human-readable time ago"""
        now = datetime.now()
        diff = now - self.created_at

        seconds = diff.total_seconds()

        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 172800:  # 2 days
            return "Yesterday"
        elif seconds < 604800:  # 7 days
            days = int(seconds / 86400)
            return f"{days} days ago"
        else:
            return self.created_at.strftime('%b %d, %Y')


class DiscussionReply(db.Model):
    """Model for replies to discussion posts"""
    __tablename__ = 'discussion_replies'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('discussion_posts.id'), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<DiscussionReply by {self.author_name}>'

    def time_ago(self):
        """Return human-readable time ago"""
        now = datetime.now()
        diff = now - self.created_at

        seconds = diff.total_seconds()

        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 172800:  # 2 days
            return "Yesterday"
        elif seconds < 604800:  # 7 days
            days = int(seconds / 86400)
            return f"{days} days ago"
        else:
            return self.created_at.strftime('%b %d, %Y')
