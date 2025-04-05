import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:root123@mediaamp-db-1:5432/taskmanager')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0') 