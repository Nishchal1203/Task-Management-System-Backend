from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from celery import Celery
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

def make_celery(app):
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
    return celery 