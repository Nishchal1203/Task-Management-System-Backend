from datetime import datetime
from app import db
from sqlalchemy import Index
from werkzeug.security import check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = db.relationship('TaskManager', backref='user', lazy=True)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TaskManager(db.Model):
    __tablename__ = 'task_manager'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='pending')
    priority = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_task_manager_status', 'status'),
        Index('idx_task_manager_user', 'user_id'),
    )

class TaskLogger(db.Model):
    __tablename__ = 'task_logger'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task_manager.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    logged_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_task_logger_date', 'logged_date'),
        Index('idx_task_logger_task', 'task_id'),
    ) 