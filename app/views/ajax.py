# Flask modules
from flask import (
    abort,
    request,
    make_response,
    Blueprint,
    url_for,
)


# App modules
from app.extensions.flask_limiter import limiter
from app.utils.response import json_response
from app.utils.reddit import get_video_path, download_video
from app.utils.errors import BadRequest

ajax_bp = Blueprint("ajax", __name__, url_prefix="/ajax")


@ajax_bp.route("/download")
@limiter.limit("10 per minutes")
async def download_reddit_video():
    url = request.args.get("url", "").strip()
    if not url:
        raise BadRequest("No reddit post url was provided.")

    media_path = await get_video_path(url)
    if media_path:
        media_url = url_for("views.media.media_url", filename=media_path)
        return json_response({"media": media_url})

    media_path = await download_video(url)
    media_url = url_for("views.media.media_url", filename=media_path)
    return json_response({"media": media_url})


@ajax_bp.route("/set-theme", methods=["POST"])
@limiter.exempt
def set_theme():
    theme = request.args.get("theme", "empty")
    allowed_themes = ("dark", "light")
    if theme.lower() not in allowed_themes:
        return abort(400, "Invalid theme")
    response = make_response("Theme set to " + theme)
    max_age = 86400  # 1 day
    response.set_cookie("theme", value=theme, max_age=max_age)
    return response
