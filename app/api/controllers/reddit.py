from flask_login import login_required
from app.api import api_bp


@api_bp.route("/reddit", methods=["GET"])
def get_video_info():
    return "Hello there !!"
