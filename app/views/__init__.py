from flask import Blueprint

views_bp = Blueprint("views", __name__)


from . import pages

views_bp.register_blueprint(pages.pages_bp)
