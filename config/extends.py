from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_redis import FlaskRedis

db = SQLAlchemy()
mail = Mail()
redis = FlaskRedis()

socketio = SocketIO(cors_allowed_origins="*")
