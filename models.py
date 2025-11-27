"""
Database models for Princeton Study Group Finder with User Authentication
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(UserMixin, db.Model):
    """Model for registered users"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    class_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)

    # Relationships
    hosted_study_groups = db.relationship('StudyGroup', backref='host', lazy=True, foreign_keys='StudyGroup.host_id')
    participations = db.relationship('Participant', backref='user', lazy=True, cascade='all, delete-orphan')
    discussion_posts = db.relationship('DiscussionPost', backref='author', lazy=True, cascade='all, delete-orphan')
    discussion_replies = db.relationship('DiscussionReply', backref='author', lazy=True, cascade='all, delete-orphan')
    post_votes = db.relationship('PostVote', backref='user', lazy=True, cascade='all, delete-orphan')
    reply_votes = db.relationship('ReplyVote', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_messages = db.relationship('ChatMessage', backref='author', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_study_groups_hosting(self):
        """Get study groups this user is hosting"""
        return StudyGroup.query.filter_by(host_id=self.id).order_by(StudyGroup.date_time.desc()).all()

    def get_study_groups_joined(self):
        """Get study groups this user has joined (including as host)"""
        group_ids = [p.study_group_id for p in self.participations]
        return StudyGroup.query.filter(StudyGroup.id.in_(group_ids)).order_by(StudyGroup.date_time.desc()).all() if group_ids else []

    def get_discussion_posts_created(self):
        """Get discussion posts created by this user"""
        return DiscussionPost.query.filter_by(author_id=self.id).order_by(DiscussionPost.created_at.desc()).all()

    def total_replies_count(self):
        """Count total replies made by user"""
        return len(self.discussion_replies)

    def total_karma(self):
        """Calculate total karma (sum of all post and reply scores)"""
        posts_karma = sum(post.score for post in self.discussion_posts)
        replies_karma = sum(reply.score for reply in self.discussion_replies)
        return posts_karma + replies_karma

    def top_posts(self, limit=5):
        """Get user's highest-scored posts"""
        return DiscussionPost.query.filter_by(author_id=self.id).order_by(DiscussionPost.score.desc()).limit(limit).all()

    def top_replies(self, limit=5):
        """Get user's highest-scored replies"""
        return DiscussionReply.query.filter_by(author_id=self.id).order_by(DiscussionReply.score.desc()).limit(limit).all()


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
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)  # -1 for unlimited
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    participants = db.relationship('Participant', backref='study_group', lazy=True, cascade='all, delete-orphan')
    chat_messages = db.relationship('ChatMessage', backref='study_group', lazy=True, cascade='all, delete-orphan')

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

    def user_is_participant(self, user_id):
        """Check if a user is already a participant"""
        return Participant.query.filter_by(study_group_id=self.id, user_id=user_id).first() is not None


class Participant(db.Model):
    """Model for study group participants"""
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    study_group_id = db.Column(db.Integer, db.ForeignKey('study_groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Participant {self.user.username}>'


class DiscussionPost(db.Model):
    """Model for course discussion posts"""
    __tablename__ = 'discussion_posts'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='General')
    pinned = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    replies = db.relationship('DiscussionReply', backref='post', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('PostVote', backref='post', lazy=True, cascade='all, delete-orphan')

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

    def get_user_vote(self, user_id):
        """Get user's vote on this post (1, -1, or None)"""
        vote = PostVote.query.filter_by(post_id=self.id, user_id=user_id).first()
        return vote.vote_type if vote else None

    def calculate_hot_score(self):
        """Calculate hot ranking score"""
        hours_old = (datetime.now() - self.created_at).total_seconds() / 3600
        return self.score / pow((hours_old + 2), 1.5)


class DiscussionReply(db.Model):
    """Model for replies to discussion posts"""
    __tablename__ = 'discussion_replies'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('discussion_posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    votes = db.relationship('ReplyVote', backref='reply', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<DiscussionReply by {self.author.username}>'

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

    def get_user_vote(self, user_id):
        """Get user's vote on this reply (1, -1, or None)"""
        vote = ReplyVote.query.filter_by(reply_id=self.id, user_id=user_id).first()
        return vote.vote_type if vote else None


class PostVote(db.Model):
    """Model for votes on discussion posts"""
    __tablename__ = 'post_votes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('discussion_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote_type = db.Column(db.Integer, nullable=False)  # 1 for upvote, -1 for downvote
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Unique constraint: one vote per user per post
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='_post_user_vote_uc'),)

    def __repr__(self):
        return f'<PostVote user={self.user_id} post={self.post_id} type={self.vote_type}>'


class ReplyVote(db.Model):
    """Model for votes on discussion replies"""
    __tablename__ = 'reply_votes'

    id = db.Column(db.Integer, primary_key=True)
    reply_id = db.Column(db.Integer, db.ForeignKey('discussion_replies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote_type = db.Column(db.Integer, nullable=False)  # 1 for upvote, -1 for downvote
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Unique constraint: one vote per user per reply
    __table_args__ = (db.UniqueConstraint('reply_id', 'user_id', name='_reply_user_vote_uc'),)

    def __repr__(self):
        return f'<ReplyVote user={self.user_id} reply={self.reply_id} type={self.vote_type}>'


class ChatMessage(db.Model):
    """Model for study group chat messages"""
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    study_group_id = db.Column(db.Integer, db.ForeignKey('study_groups.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<ChatMessage by {self.author.username} in group {self.study_group_id}>'

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
            return self.created_at.strftime('%b %d, %Y at %I:%M %p')
