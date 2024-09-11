from flask import request, jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from app.models import User, db

def register_routes(app):
    @app.route('/')
    @app.route('/login/', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return jsonify({'message': 'Login successful'}), 200
        elif user and user.password == password:
            return jsonify({'message': 'Login successful'}), 200
        else:
            print(check_password_hash(user.password, password))
            return jsonify({'message': 'Invalid credentials'}), 401
        
    @app.route('/register/',methods=['POST'])
    def register():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400
        
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message':'Registered successfully'}),201
        except Exception as e :
            db.session.rollback()
            return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

