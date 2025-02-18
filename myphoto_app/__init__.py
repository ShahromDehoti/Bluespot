# myphoto_app/__init__.py
from flask import Flask
from flask_login import LoginManager
from .extensions import db, socketio
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login'  # assuming login route in your blueprint

    from .models import User  # import models after initializing db
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints/routes
    from .routes import main
    app.register_blueprint(main)

    return app
