from app.api import api_bp


@api_bp.route("/reddit", methods=["GET"])
def get_users():
    return "Hello there !!"
