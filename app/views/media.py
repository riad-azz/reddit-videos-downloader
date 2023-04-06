# Flask modules
from flask import (
    Blueprint,
    send_from_directory,
)

# Other modules
import os

# App modules
from app import BASE_DIR

VIDEOS_FOLDER = os.path.join(BASE_DIR, "media/videos")

media_bp = Blueprint("media", __name__, url_prefix="/media")


@media_bp.route("/<path:filename>")
def media(filename):
    return send_from_directory(
        VIDEOS_FOLDER,
        filename,
        as_attachment=True,
    )
