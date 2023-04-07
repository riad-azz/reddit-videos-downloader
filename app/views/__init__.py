# Flask modules
from flask import Blueprint

# App modules
from app.utils.response import json_response
from app.utils.errors import HTTPException

views_bp = Blueprint("views", __name__)


from . import ajax
from . import pages

views_bp.register_blueprint(ajax.ajax_bp)
views_bp.register_blueprint(pages.pages_bp)


@views_bp.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


@views_bp.errorhandler(HTTPException)
def server_error(error: HTTPException):
    if not error.code:
        error.code = 500
    return json_response({"error": error.description}, error.code)
