# Flask modules
from flask import (
    abort,
    request,
    send_file,
    make_response,
    Blueprint,
)

# App modules
from app.utils import json_response
from app.utils import download_video, valid_reddit_post

ajax_bp = Blueprint("ajax", __name__, url_prefix="/ajax")


@ajax_bp.app_errorhandler(500)
def server_error(error):
    return json_response({"error": "500 Internal server error"})


@ajax_bp.route("/download/<url>", methods=["GET"])
async def download_reddit_video(url: str):
    valid_url = valid_reddit_post(url)
    if not valid_url:
        return json_response({"error": "Invalid reddit post url"})

    try:
        media_path = await download_video(valid_url)
    except Exception as e:
        return json_response({"error": str(e)})

    return send_file(media_path, as_attachment=True)


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
