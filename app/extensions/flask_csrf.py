# Flask modules
from flask import current_app
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(current_app)
