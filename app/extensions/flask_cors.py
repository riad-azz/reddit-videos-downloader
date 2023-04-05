# Flask modules
from flask import current_app
from flask_cors import CORS


cors = CORS(current_app, resources={r"/api/*": {"origins": "*"}})
