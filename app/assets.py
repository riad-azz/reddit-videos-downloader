import os
import shutil
from app import app
from flask_assets import Environment, Bundle

assets = Environment(app)
assets.cache = True
assets.url = app.static_url_path
assets.directory = app.static_folder

# CSS BUNDLES
assets.register(
    "css_all",
    Bundle(
        "css/main.css",
        "css/style.css",
        output="gen/style.css",
        filters="cssmin",
    ),
)

# JAVASCRIPT BUNDLES
assets.register(
    "js_head",
    Bundle(
        "js/theme.js",
        output="gen/head.js",
        filters="jsmin",
    ),
)

assets.register(
    "js_defer",
    Bundle(
        "js/main.js",
        output="gen/defer.js",
        filters="jsmin",
    ),
)

# Clear the Flask-Assets cache
CACHE_DIR = os.path.join(app.static_folder, ".webassets-cache")
if os.path.exists(CACHE_DIR):
    shutil.rmtree(CACHE_DIR)
