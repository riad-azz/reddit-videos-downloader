# Flask modules
from flask import (
    abort,
    request,
    Blueprint,
    send_file,
    make_response,
)


# App modules
from app.extensions.flask_limiter import limiter
from app.utils.errors import BadRequest
from app.utils.reddit import (
    get_video,
    download_video,
    validate_video_url,
    validate_audio_url,
)
from app.utils.response import json_response

ajax_bp = Blueprint("ajax", __name__, url_prefix="/ajax")


# post_url = "https://www.reddit.com/r/PeopleFuckingDying/comments/12eoavt/exclusive_footage_of_ferocious_lion_stalking_its"
# video_url="https://v.redd.it/f6giymkr9hsa1/DASH_220.mp4",
# audio_url="https://v.redd.it/f6giymkr9hsa1/DASH_audio.mp4",


@ajax_bp.route("/download")
@limiter.limit("10 per minutes")
async def download_reddit_video():
    title = request.args.get("title", "")
    video_url = request.args.get("video", "").strip()
    audio_url = request.args.get("audio", "").strip()
    if not title or not video_url or not audio_url:
        raise BadRequest("Bad request, missing parameters")
    validate_video_url(video_url)
    validate_audio_url(audio_url)

    filename = title + ".mp4"
    video_file = await download_video(video_url, audio_url)

    return send_file(
        video_file,
        download_name=filename,
        as_attachment=True,
    )


@ajax_bp.route("/fetch")
@limiter.limit("10 per minutes")
async def fetch_reddit_video():
    url = request.args.get("url", "").strip()
    if not url:
        raise BadRequest("No post url was provided.")

    video_info = await get_video(url)

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
