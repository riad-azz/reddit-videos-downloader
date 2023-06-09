# Flask modules
from flask import current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# App modules
from app.utils.response import json_response

limiter = Limiter(
    get_remote_address,
    app=current_app,
    default_limits=["10 per minute"],
    storage_uri="memory://",
)


@current_app.errorhandler(429)
def rate_limit_handler(error):
    return json_response({"error": f"{error}. try again in later."}, 429)
