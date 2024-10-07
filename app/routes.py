from flask import redirect, request, jsonify, session, url_for
from werkzeug.security import check_password_hash,generate_password_hash
from app.models import User, UserFiles, db
import os

def get_user_id_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.id
    else:
      return None
def user_directory(model_name,username):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),''))
    data_dir = os.path.join(base_dir,'Data',model_name,username)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir


# REGISTER_ROUTES
def register_routes(app):
    @app.route('/',methods=['POST'])
    def home():
        print('session là: ' + str(session))
        print('User ID: ' + str(User.id))
        if 'user_id' in session:
            # return redirect(url_for('login'))
            return jsonify({'message': 'Welcome to the homepage! You are already logged in.'}), 200
        else:
            return redirect(url_for('login'))
    @app.route('/login/', methods=['POST', 'GET'])
    def login():
        if request.method != 'GET':
            # Nếu người dùng truy cập qua GET, trả về trang đăng nhập
            return jsonify({'message': 'Please log in'}), 401
        
        # data = request.json
        data = {
            'username' :'biomodel',
            'password' : '123456'
        }
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username='biomodel').first()

        
        if user and (check_password_hash(user.password, password) or user.password == '123456'): 
            # Lưu thông tin người dùng vào session
            session['user_id'] = user.id
            print(user, user.password)
            return jsonify({'message': 'Login successful'}), 200
        else:
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
        
    @app.route('/storeSkinCancer/',methods=['POST'])
    def storeSkinCancer():
        model_name = 'SkinCancer'

        data = request
        username = data.form.get('user')
        picture =  data.files['image']

        user = User.query.filter_by(username=username).first() 
        user_dir = user_directory(model_name=model_name,username=username)

        file_path = os.path.join(user_dir,picture.filename)

        try:
            picture.save(file_path)
        except Exception as e:
            return jsonify({"message":f'{str(e)}'})
        
        existing_file = UserFiles.query.filter_by(file_name=picture.filename, file_path=file_path).first()

        if existing_file:
            return jsonify({"message": "File with the same name and path already exists."})

        user_file = UserFiles(user_id=user.id,file_name=picture.filename,file_path=file_path)

        try:
            db.session.add(user_file)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f'{str(e)}'})

        return jsonify({"":'Successfully'})
    
    @app.route('/historyFiles/',methods=['POST'])
    def historyFiles():
        user_id = get_user_id_by_username('biomodel')
        files_list = UserFiles.query.filter_by(user_id=user_id).all()
        return jsonify([file.serialize() for file in files_list])
    
    @app.route('/deleteFileResult/',methods=['POST'])
    def delFileResult():
        user_id = get_user_id_by_username('biomodel')
        data = request
        del_id = data.form.get('id')

        file = UserFiles.query.filter_by(id = del_id).first()
        if file:
            try:
                if os.path.exists(file.file_path):
                    os.remove(file.file_path)  
                    print(file.file_path)

                db.session.delete(file)
                db.session.commit()

                return jsonify({"message": "File deleted successfully"})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"message": "File not found"})


