from flask import Blueprint

views_bp = Blueprint("views", __name__)


from . import ajax
from . import pages


views_bp.register_blueprint(ajax.ajax_bp)
views_bp.register_blueprint(pages.pages_bp)
