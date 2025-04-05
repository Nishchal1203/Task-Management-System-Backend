from celery import Celery
from app import create_app, db
from app.models import TaskManager, TaskLogger
from datetime import datetime, date
import logging

app = create_app()
celery = Celery(
    app.import_name,
    broker=app.config['REDIS_URL'],
    backend=app.config['REDIS_URL']
)

celery.conf.update(app.config)

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

@celery.task
def load_daily_tasks():
    """Daily task to transfer active tasks from TaskManager to TaskLogger"""
    try:
        today = date.today()
        
        # Check if tasks for today are already logged
        existing_logs = TaskLogger.query.filter_by(logged_date=today).first()
        if existing_logs:
            logging.info(f"Tasks for {today} already logged")
            return
        
        # Get all active tasks
        active_tasks = TaskManager.query.filter_by(is_active=True).all()
        
        for task in active_tasks:
            # Create a new log entry
            task_log = TaskLogger(
                task_id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                priority=task.priority,
                user_id=task.user_id,
                logged_date=today
            )
            db.session.add(task_log)
        
        db.session.commit()
        logging.info(f"Successfully logged {len(active_tasks)} tasks for {today}")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in daily task loading: {str(e)}")
        raise 