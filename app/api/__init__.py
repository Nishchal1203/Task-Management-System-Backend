from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.models import TaskManager, TaskLogger, User
from app import db
from datetime import datetime
import pandas as pd
from io import StringIO
from functools import wraps
from werkzeug.security import generate_password_hash

api_bp = Blueprint('api', __name__)

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = User.query.filter_by(id=get_jwt_identity()).first()
            if not current_user or current_user.role != role:
                return jsonify({'error': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'user')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=str(user.id))  # Ensure identity is a string

    return jsonify({'access_token': access_token}), 200

@api_bp.route('/upload-csv', methods=['POST'])
@jwt_required()
@role_required('admin')
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400

    try:
        df = pd.read_csv(StringIO(file.read().decode('utf-8')))

        for _, row in df.iterrows():
            # Convert status string to boolean
            status_str = str(row.get('status', 'FALSE')).strip().lower()
            status = True if status_str == 'true' else False

            # Parse created_at if it's part of the model
            created_at = datetime.strptime(str(row['created_at']), "%m/%d/%Y")

            # Get the user by username (assigned_user)
            assigned_username = row.get('assigned_user', '').strip()
            user = User.query.filter_by(username=assigned_username).first()

            if not user:
                continue  # Or log and skip this task

            task = TaskManager(
                title=row['task_name'],
                description=row.get('description', ''),
                status=status,
                priority=row.get('priority', 'MEDIUM'),
                user_id=user.id,
                created_at=created_at  # Only if your model has this field
            )
            db.session.add(task)

        db.session.commit()
        return jsonify({'message': 'Tasks uploaded successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    date = request.args.get('date')
    
    query = TaskLogger.query
    
    if date:
        query = query.filter(TaskLogger.logged_date == datetime.strptime(date, '%Y-%m-%d').date())
    
    tasks = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'tasks': [{
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'logged_date': task.logged_date.isoformat()
        } for task in tasks.items],
        'total': tasks.total,
        'pages': tasks.pages,
        'current_page': tasks.page
    })

@api_bp.route('/task/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    task = TaskLogger.query.get_or_404(task_id)
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'logged_date': task.logged_date.isoformat()
    })

@api_bp.route('/task', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    task = TaskManager(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'MEDIUM'),
        user_id=current_user_id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'status': task.status
    }), 201

@api_bp.route('/task/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = TaskManager.query.get_or_404(task_id)
    current_user_id = get_jwt_identity()
    
    if task.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    
    db.session.commit()
    return jsonify({
        'id': task.id,
        'title': task.title,
        'status': task.status
    })

@api_bp.route('/task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = TaskManager.query.get_or_404(task_id)
    current_user_id = get_jwt_identity()
    
    if task.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    task.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'}) 