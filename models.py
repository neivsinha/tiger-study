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

    # Relationship to study groups
    study_groups = db.relationship('StudyGroup', backref='course', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Course {self.code}: {self.title}>'

    def active_study_groups_count(self):
        """Count active (future) study groups for this course"""
        return StudyGroup.query.filter(
            StudyGroup.course_id == self.id,
            StudyGroup.date_time >= datetime.now()
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
