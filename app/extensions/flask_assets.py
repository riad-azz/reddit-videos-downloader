# Flask modules
from flask import current_app, request
from flask_assets import Environment, Bundle

# Other modules
import os
import shutil
import secrets

NAMES_USED = list()


def random_name(length: int = 8):
    name = secrets.token_hex(length)
    while name in NAMES_USED:
        name = secrets.token_hex(length)
    return name


def generate_asset_path(extension: str = "js", path: str = "assets"):
    if not path.endswith("/"):
        path + "/"
    asset_path = path + "/" + random_name() + "." + extension
    return asset_path


assets = Environment(current_app)
assets.cache = True
assets.url = current_app.static_url_path
assets.directory = current_app.static_folder

# CSS BUNDLES
assets.register(
    "css_all",
    Bundle(
        "css/main.css",
        "css/style.css",
        output=generate_asset_path("css"),
        filters="cssmin",
    ),
)

# JAVASCRIPT BUNDLES
assets.register(
    "js_head",
    Bundle(
        "js/theme.js",
        output=generate_asset_path("js"),
        filters="jsmin",
    ),
)

assets.register(
    "js_defer",
    Bundle(
        "js/main.js",
        output=generate_asset_path("js"),
        filters="jsmin",
    ),
)

assets.register(
    "reddit_script",
    Bundle(
        "js/reddit-script.js",
        output=generate_asset_path("js"),
        filters="jsmin",
    ),
)

# CLEAR FLASK-ASSETS CACHE
CACHE_DIR = os.path.join(current_app.static_folder, ".webassets-cache")
if os.path.exists(CACHE_DIR):
    shutil.rmtree(CACHE_DIR)
OLD_DIR = os.path.join(current_app.static_folder, "assets")
if os.path.exists(OLD_DIR):
    shutil.rmtree(OLD_DIR)


# CACHE STATIC FILES
@current_app.after_request
def add_cache_header(response):
    if request.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000"
    return response
