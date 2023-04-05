# Flask modules
from flask import Flask

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
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# APP ROUTES
from app.views import views_bp

app.register_blueprint(views_bp)
# API ROUTES
from app.api import api_bp

app.register_blueprint(api_bp)

# APP EXTENSIONS
from app import extensions
