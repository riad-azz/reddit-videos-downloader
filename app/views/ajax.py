# Flask modules
from flask import (
    abort,
    request,
    Blueprint,
    send_file,
    make_response,
    after_this_request,
)

# Other modules
import uuid


# App modules
from app.utils.errors import BadRequest
from app.utils.response import json_response
from app.utils.validators import validate_video_url, validate_audio_url
from app.utils.reddit import get_video, download_video, TEMP_FOLDER
from app.extensions.flask_limiter import limiter
from app.forms.ajax import FetchForm

ajax_bp = Blueprint("ajax", __name__, url_prefix="/ajax")


@ajax_bp.route("/download")
@limiter.limit("10 per minutes")
async def download_reddit_video():
    title = request.args.get("title", "reddit_video")
    video_url = request.args.get("video", "").strip()
    audio_url = request.args.get("audio", "").strip()
    if not title or not video_url or not audio_url:
        raise BadRequest("Bad request, missing parameters")
    validate_video_url(video_url)
    validate_audio_url(audio_url)

    folder_name = str(uuid.uuid4())

    filename = title + ".mp4"
    video_file = await download_video(video_url, audio_url, folder_name)

    response = send_file(
        video_file,
        download_name=filename,
        as_attachment=True,
    )
    response.set_cookie("temp", value=folder_name, max_age=3600)
    return response


@ajax_bp.route("/fetch", methods=["POST"])
@limiter.limit("10 per minutes")
async def fetch_reddit_video():
    form = FetchForm(request.form)
    if not form.validate():
        error = list(form.errors.values())[-1][-1]
        raise BadRequest(error)

    post_url = form.url.data
    video_info = await get_video(post_url)

    filename = video_info["title"] + ".mp4"
    download_url = video_info["download_url"]
    response = {
        "success": True,
        "filename": filename,
        "download_url": download_url,
    }
    return json_response(response, 200)


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
