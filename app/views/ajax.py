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
from app.utils.formatters import sanitize_text
from app.utils.reddit import download_video, validate_audio_url, validate_video_url

ajax_bp = Blueprint("ajax", __name__, url_prefix="/ajax")


@ajax_bp.route("/download")
@limiter.limit("10 per minutes")
async def download_reddit_video():
    title = request.args.get("title", "reddit_video")
    sanitized_title = sanitize_text(title)

    video_url = request.args.get("video", "").strip()
    audio_url = request.args.get("audio", "").strip()
    valid_video = validate_video_url(video_url)
    valid_audio = validate_audio_url(audio_url)

    # video_url="https://v.redd.it/f6giymkr9hsa1/DASH_220.mp4",
    # audio_url="https://v.redd.it/f6giymkr9hsa1/DASH_audio.mp4",

    media_file = await download_video(
        video_url=valid_video,
        audio_url=valid_audio,
    )

    filename = sanitized_title + ".mp4"
    return send_file(
        media_file,
        download_name=filename,
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
