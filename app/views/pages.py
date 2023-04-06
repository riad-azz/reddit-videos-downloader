# Flask modules
from flask import (
    render_template,
    Blueprint,
)

# App modules
from app.extensions.flask_limiter import limiter

pages_bp = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages_bp.route("/")
@limiter.exempt
def home_page():
    return render_template("home.html")
