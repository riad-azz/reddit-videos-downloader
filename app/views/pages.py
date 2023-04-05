# Flask modules
from flask import (
    abort,
    make_response,
    render_template,
    Blueprint,
)
from flask_login import login_required


pages_bp = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages_bp.route("/")
def home_page():
    return render_template("home.html")


@pages_bp.route("/my-api")
def api_page():
    return render_template("api.html")


@pages_bp.route("/set-theme/<theme>", methods=["GET"])
def set_theme(theme: str):
    allowed_themes = ("dark", "light")
    if theme.lower() not in allowed_themes:
        return abort(400, "Invalid theme")
    response = make_response("Theme set to " + theme)
    max_age = 86400  # 1 day
    response.set_cookie("theme", value=theme, max_age=max_age)
    return response
