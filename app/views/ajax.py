# Flask modules
import os
from flask import (
    abort,
    request,
    Blueprint,
    send_file,
    make_response,
    after_this_request,
)


# App modules
from app.extensions.flask_limiter import limiter
from app.utils.response import json_response
from app.utils.reddit import download_video
from app.utils.errors import BadRequest

ajax_bp = Blueprint("ajax", __name__, url_prefix="/ajax")


@ajax_bp.route("/download")
@limiter.limit("10 per minutes")
async def download_reddit_video():
    url = request.args.get("url", "").strip()
    if not url:
        raise BadRequest("No reddit post url was provided.")

    media_file = await download_video(
        video_url="https://v.redd.it/f6giymkr9hsa1/DASH_220.mp4",
        audio_url="https://v.redd.it/f6giymkr9hsa1/DASH_audio.mp4",
    )

    return send_file(
        media_file,
        download_name="potato.mp4",
        as_attachment=True,
    )


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
