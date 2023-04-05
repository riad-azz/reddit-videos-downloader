# Flask modules
from flask import (
    abort,
    make_response,
    render_template,
    Blueprint,
)


pages_bp = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages_bp.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


@pages_bp.route("/")
def home_page():
    return render_template("home.html")
