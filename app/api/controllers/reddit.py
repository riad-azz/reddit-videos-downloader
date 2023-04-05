# Flask modules
from flask_cors import cross_origin

# App modules
from app.api import api_bp
from app.api.utils import json_response


@api_bp.route("/reddit", methods=["GET"])
@cross_origin()
def get_video_info():
    data = {
        "video": {
            "title": "Title",
            "duration": "4:12",
            "videoUrl": "reddit.com/{POST_ID}/video_240.mp4?source=fallback",
            "audioUrl": "reddit.com/{POST_ID}/audio.mp4",
        }
    }
    return json_response(data)
