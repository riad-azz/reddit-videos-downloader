# Flask modules
from flask import (
    Blueprint,
    send_file,
    after_this_request,
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
@limiter.limit("10 per 1 minutes")
@cross_origin()
def media_url(filename):
    @after_this_request
    def remove_file(response):
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as error:
            print("Error removing or closing downloaded file handle", error)
        return response

    return send_file(
        VIDEOS_FOLDER,
        filename,
        as_attachment=True,
    )
