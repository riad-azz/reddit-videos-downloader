# Flask modules
from flask import Flask

# Other modules
import os
from pathlib import Path

# App modules
from app import config

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = os.path.join(BASE_DIR, "static")
MEDIA_DIR = os.path.join(BASE_DIR, "MEDIA")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


def create_app(debug=False):
    # INIT FLASK APP
    app = Flask(
        __name__,
        static_folder=STATIC_DIR,
        static_url_path="/static/",
        template_folder=TEMPLATE_DIR,
    )

    # APP CONFIGS
    if debug:
        app.config.from_object(config.dev_config.Config)
    else:
        app.config.from_object(config.prod_config.Config)

    # PUSH APP CONTEXT
    app.app_context().push()

    # APP EXTENSIONS
    from app import extensions

    # APP ROUTES
    from app.views import views_bp

    app.register_blueprint(views_bp)

    return app
