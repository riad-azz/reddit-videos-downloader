# Flask modules
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Other modules
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# INIT FLASK APP
app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    static_url_path="/static/",
    template_folder=TEMPLATE_DIR,
)

# APP CONFIGS
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR}/database/database.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# DATABASE
db = SQLAlchemy(app)
# ENCRYPTION
bcrypt = Bcrypt(app)
# AUTHENTICATION
login_manager = LoginManager(app)
login_manager.login_view = "views.auth.login_page"
login_manager.login_message = "Please sign in to continue."
login_manager.login_message_category = "info"

# APP MODELS
from app import models

with app.app_context():
    db.create_all()

# APP ROUTES
from app.views import views_bp

app.register_blueprint(views_bp)
# API ROUTES
from app.api import api_bp

app.register_blueprint(api_bp)

# APP EXTENSIONS
from app import extensions
