# Other modules
import io
import os
import re
import ffmpeg
import asyncio
from tempfile import NamedTemporaryFile

# App modules
from app import BASE_DIR
from .http import get_media_bytes, get_post_json, get_post_mpd
from .formatters import format_post_json, format_mpd
from .errors import ServerError, BadRequest, HTTPException

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


async def download_video(video_url: str, audio_url: str) -> str:
    video_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=TEMP_FOLDER)
    audio_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=TEMP_FOLDER)
    output_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=TEMP_FOLDER)
    try:
        video_buffer, audio_buffer = await asyncio.gather(
            get_media_bytes(video_url),
            get_media_bytes(audio_url),
        )
        video_file.write(video_buffer)
        audio_file.write(audio_buffer)

        input_video = ffmpeg.input(video_file.name)
        input_audio = ffmpeg.input(audio_file.name)

        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(
            output_file.name, loglevel="quiet"
        ).run(overwrite_output=True, capture_stdout=False, capture_stderr=False)

        media_file = io.BytesIO(output_file.read())
        return media_file

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        else:
            print(e)
            raise ServerError("Could not process the video & audio files.")
    finally:
        output_file.close()
        os.unlink(output_file.name)
        video_file.close()
        os.unlink(video_file.name)
        audio_file.close()
        os.unlink(audio_file.name)


async def get_video_info(post_url: str) -> dict:
    valid_url = validate_post_url(post_url)

    post_json = await get_post_json(valid_url)
    post_json = format_post_json(post_json)
    title = post_json["title"]
    url = post_json["url"]
    dash_url = post_json["dash_url"]

    post_mpd = await get_post_mpd(dash_url)
    video_info = format_mpd(post_mpd, url)
    video_info["title"] = title

    return video_info
