# Flask modules
from flask import Blueprint, request

# Other modules
import os
import shutil

# App modules
from app.utils.response import json_response
from app.utils.errors import HTTPException
from app.utils.reddit import TEMP_FOLDER

views_bp = Blueprint("views", __name__)


from . import ajax
from . import pages

views_bp.register_blueprint(ajax.ajax_bp)
views_bp.register_blueprint(pages.pages_bp)


@views_bp.after_request
def after_reddit_download(response):
    if request.path == "/ajax/download":
        cookies = request.cookies
        folder_name = cookies.get("temp", "/doesntexist")
        response.set_cookie("temp", value="", max_age=0)
        folder_path = TEMP_FOLDER / folder_name
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
    return response


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
