# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"
login_manager = LoginManager()
mail = Mail()   

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'tan.negi19@gmail.com'
    app.config['MAIL_PASSWORD'] = 'bkpzengbpqmanasu'
    app.config['MAIL_DEFAULT_SENDER'] = 'tan.negi19@gmail.com' 

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)   
    migrate = Migrate(app, db)

    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .auth import auth
    from .routes import routes, doctors_bp
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(doctors_bp)

    # User loader
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
