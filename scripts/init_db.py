from app import create_app, db
from app.models import User, TaskManager
from datetime import datetime
import os

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create users
        users = {
            'john_doe': User(username='john_doe', password_hash='hashed_password1', role='admin'),
            'jane_smith': User(username='jane_smith', password_hash='hashed_password2', role='user'),
            'mark_jones': User(username='mark_jones', password_hash='hashed_password3', role='user'),
            'lisa_adams': User(username='lisa_adams', password_hash='hashed_password4', role='user'),
            'emma_watson': User(username='emma_watson', password_hash='hashed_password5', role='user'),
            'robert_brown': User(username='robert_brown', password_hash='hashed_password6', role='user')
        }
        
        # Add users to database
        for user in users.values():
            db.session.add(user)
        db.session.commit()
        
        # Create tasks
        tasks = [
            {
                'title': 'Data Backup',
                'description': 'Backup database daily',
                'status': 'active',
                'priority': 'HIGH',
                'created_at': datetime(2025, 3, 31),
                'assigned_user': 'john_doe'
            },
            {
                'title': 'Security Audit',
                'description': 'Review system security',
                'status': 'active',
                'priority': 'MEDIUM',
                'created_at': datetime(2025, 3, 30),
                'assigned_user': 'jane_smith'
            },
            {
                'title': 'API Performance Test',
                'description': 'Run load tests on APIs',
                'status': 'active',
                'priority': 'HIGH',
                'created_at': datetime(2025, 3, 28),
                'assigned_user': 'mark_jones'
            },
            {
                'title': 'Code Review',
                'description': 'Review PRs and merge pending code',
                'status': 'active',
                'priority': 'MEDIUM',
                'created_at': datetime(2025, 3, 29),
                'assigned_user': 'lisa_adams'
            },
            {
                'title': 'Server Update',
                'description': 'Update production servers',
                'status': 'active',
                'priority': 'HIGH',
                'created_at': datetime(2025, 4, 1),
                'assigned_user': 'john_doe'
            },
            {
                'title': 'Error Log Analysis',
                'description': 'Analyze recent server errors',
                'status': 'inactive',
                'priority': 'LOW',
                'created_at': datetime(2025, 3, 31),
                'assigned_user': 'emma_watson'
            },
            {
                'title': 'Feature Deployment',
                'description': 'Deploy new feature release',
                'status': 'inactive',
                'priority': 'CRITICAL',
                'created_at': datetime(2025, 4, 2),
                'assigned_user': 'robert_brown'
            }
        ]
        
        # Add tasks to database
        for task_data in tasks:
            user = users[task_data['assigned_user']]
            task = TaskManager(
                title=task_data['title'],
                description=task_data['description'],
                status=task_data['status'],
                priority=task_data['priority'],
                created_at=task_data['created_at'],
                user_id=user.id,
                is_active=task_data['status'] == 'active'
            )
            db.session.add(task)
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 