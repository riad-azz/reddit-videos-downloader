# Flask modules
from flask import (
    abort,
    request,
    make_response,
    Blueprint,
)


ajax_bp = Blueprint("ajax", __name__, url_prefix="/ajax")


@ajax_bp.route("/set-theme", methods=["POST"])
def set_theme():
    theme = request.args.get("theme", "empty")
    allowed_themes = ("dark", "light")
    if theme.lower() not in allowed_themes:
        return abort(400, "Invalid theme")
    response = make_response("Theme set to " + theme)
    max_age = 86400  # 1 day
    response.set_cookie("theme", value=theme, max_age=max_age)
    return response
