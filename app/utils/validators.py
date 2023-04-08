# Other modules
import re

# App modules
from app import BASE_DIR
from .errors import BadRequest

TEMP_FOLDER = BASE_DIR / "media/temp"


def validate_video_url(url: str):
    pattern = r"https://v\.redd\.it\/\w+\/DASH_(\d+)\.mp4"
    match = re.match(pattern, url)
    if match:
        valid_url = match.group()
        return valid_url
    else:
        raise BadRequest("Invalid reddit audio url provided.")


def validate_audio_url(url: str):
    pattern = r"https://v\.redd\.it\/\w+\/DASH_audio\.mp4"
    match = re.match(pattern, url)
    if match:
        valid_url = match.group()
        return valid_url
    else:
        raise BadRequest("Invalid reddit audio url provided.")


def validate_post_url(url: str) -> str:
    pattern = r"(?:https?://)?(?:www\.)?reddit\.com/r/\w+/comments/\w+/?"
    match = re.match(pattern, url)
    if match:
        valid_url = match.group()
        return valid_url
    else:
        raise BadRequest("Invalid reddit post url provided.")
