from flask import Flask
from flask_cors import CORS
from app.routes import *
from app.models import *

app = Flask(__name__)

# Cấu hình cơ sở dữ liệu
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./instance/users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/NAMPC/Documents/GeneStory/biomodel/backendFlask/instance/users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r"/*": {"origins": "*"}})

# Khởi tạo đối tượng SQLAlchemy với ứng dụng
db.init_app(app)

register_routes(app)
if __name__ == '__main__':
    app.run(debug=True)
