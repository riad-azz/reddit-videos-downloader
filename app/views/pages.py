# Flask modules
from flask import (
    request,
    render_template,
    Blueprint,
)

# App modules
from app.extensions.flask_limiter import limiter
from app.utils.reddit import (
    get_video_info,
    validate_post_url,
)

pages_bp = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages_bp.route("/")
@limiter.exempt
def home_page():
    return render_template("home.html")


@pages_bp.route("/info", methods=["POST", "GET"])
@limiter.exempt
async def info_page():
    if request.method == "GET":
        return render_template("empty.html")

    post_url = request.form.get("url", "")
    try:
        valid_url = validate_post_url(post_url)
    except:
        return render_template("empty.html")

    video_info = await get_video_info(valid_url)

    return render_template("info.html", info=video_info)
