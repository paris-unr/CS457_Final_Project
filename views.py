from flask import Blueprint, jsonify, request, session
from models import db, User
from controller import import_csv

main = Blueprint('main', __name__)

@main.route('/')
def index():
    import_csv()
    return jsonify({'message': 'Welcome to the API!'})

@main.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    try:
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully!',
            'user': new_user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.password == data['password']:
        session['user_id'] = user.id
        session['username'] = user.username
        
        return jsonify({
            'message': 'Login successful!',
            'user': user.to_dict()
        }), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401

@main.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logged out successfully!'}), 200

@main.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@main.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200