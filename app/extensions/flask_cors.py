# Flask modules
from flask_cors import CORS

# App modules
from app import app

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
