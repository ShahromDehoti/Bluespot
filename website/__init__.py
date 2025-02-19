# myphoto_app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    from .models import User
    with app.app_context():
        db.create_all()

    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login'  # assuming login route in your blueprint

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    return app
