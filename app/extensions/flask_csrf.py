# Flask modules
from flask_wtf.csrf import CSRFProtect

# App modules
from app import app

csrf = CSRFProtect(app)
