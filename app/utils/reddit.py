# Other modules
import os
import re
import ffmpeg
import asyncio
import requests
from tempfile import NamedTemporaryFile

# App modules
from app import BASE_DIR
from .formatters import format_video_json
from .errors import ServerError, BadRequest, HTTPException

VIDEOS_FOLDER = BASE_DIR / "media/videos"
TEMP_FOLDER = BASE_DIR / "media/temp"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
}


def sanitize_text(text: str) -> str:
    return re.sub(r"[^\w\s-]", "", text)


def get_filename(post_url: str) -> str:
    url_parts = post_url.split("/")
    post_id = sanitize_text(url_parts[6])
    post_title = sanitize_text(url_parts[7])
    filename = post_title + "_" + post_id + ".mp4"
    return filename


def validate_post_url(url: str) -> str:
    pattern = r"(?:https?://)?(?:www\.)?reddit\.com/r/\w+/comments/\w+/?"
    match = re.match(pattern, url)
    if match:
        valid_url = match.group()
        return valid_url
    else:
        raise BadRequest("Invalid reddit post url provided.")


def is_video_exist(filename: str) -> bool:
    file_path = os.path.join(VIDEOS_FOLDER, filename)
    return os.path.exists(file_path)


async def get_media_buffer(url: str) -> NamedTemporaryFile:
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 404:
        raise BadRequest("404 Post media files not found.")
    if response.status_code != 200:
        raise ServerError(
            f"{response.status_code} Could not fetch the video. Request denied by reddit.com."
        )
    return response.content


async def get_post_json(url: str) -> dict:
    json_url = url + ".json"
    response = requests.get(json_url, headers=HEADERS)
    if response.status_code != 200:
        raise ServerError("Could not connect to reddit.com.")

    if not "application/json" in response.headers.get("Content-Type", ""):
        raise BadRequest("404 Post was not found.")

    return response.json()


async def download_media(
    video_url: str, audio_url: str, filename: str = "reddit_video.mp4"
) -> str:
    video_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=TEMP_FOLDER)
    audio_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=TEMP_FOLDER)
    try:
        video_buffer, audio_buffer = await asyncio.gather(
            get_media_buffer(video_url), get_media_buffer(audio_url)
        )
        video_file.write(video_buffer)
        audio_file.write(audio_buffer)

        input_video = ffmpeg.input(video_file.name)
        input_audio = ffmpeg.input(audio_file.name)

        output_path = os.path.join(VIDEOS_FOLDER, filename)

        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(
            output_path, loglevel="quiet"
        ).run(overwrite_output=True, capture_stdout=False, capture_stderr=False)

        return output_path

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        else:
            raise ServerError("Could not process the video & audio files.")
    finally:
        video_file.close()
        os.unlink(video_file.name)
        audio_file.close()
        os.unlink(audio_file.name)


async def get_video_path(post_url: str) -> str | None:
    valid_url = validate_post_url(post_url)
    filename = get_filename(post_url)

    video_exist = is_video_exist(filename)
    if video_exist:
        return filename
    else:
        return None


async def download_video(post_url: str) -> str:
    valid_url = validate_post_url(post_url)
    filename = get_filename(post_url)

    post_json = await get_post_json(valid_url)
    video_obj = format_video_json(post_json)
    video_url = video_obj["video_url"]
    audio_url = video_obj["audio_url"]
    # Wait for the file to download and be saved
    await download_media(
        video_url=video_url,
        audio_url=audio_url,
        filename=filename,
    )
    return filename
