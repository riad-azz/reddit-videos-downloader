# Other modules
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    TEMPLATES_AUTO_RELOAD = True
