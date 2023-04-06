# Flask modules
from flask import (
    Blueprint,
    send_from_directory,
)
from flask_cors import cross_origin

# Other modules
import os

# App modules
from app import BASE_DIR
from app.extensions.flask_limiter import limiter

VIDEOS_FOLDER = os.path.join(BASE_DIR, "media/videos")

media_bp = Blueprint("media", __name__, url_prefix="/media")


@media_bp.route("/<path:filename>")
@limiter.limit("1 per 10 minutes")
@cross_origin()
def media_url(filename):
    return send_from_directory(
        VIDEOS_FOLDER,
        filename,
        as_attachment=True,
    )
