from flask import Blueprint

views_bp = Blueprint("views", __name__)

from . import auth
from . import pages

views_bp.register_blueprint(auth.auth_bp)
views_bp.register_blueprint(pages.pages_bp)
