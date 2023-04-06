# Other modules
import os
import re
import ffmpeg
import asyncio
import requests
from tempfile import NamedTemporaryFile

# App modules
from app import BASE_DIR

VIDEOS_FOLDER = BASE_DIR / "media/videos"
TEMP_FOLDER = BASE_DIR / "media/temp"


def sanitize_text(text: str) -> str:
    return re.sub(r"[^\w\s-]", "", text)


def get_filename(post_url: str) -> str:
    url_parts = post_url.split("/")
    post_id = sanitize_text(url_parts[6])
    post_title = sanitize_text(url_parts[7])
    filename = post_id + "_" + post_title + ".mp4"
    return filename


def valid_reddit_post(url: str) -> str | None:
    pattern = r"(?:https?://)?(?:www\.)?reddit\.com/r/\w+/comments/\w+/?"
    match = re.match(pattern, url)
    if match:
        return match.group()
    else:
        return None


def is_video_exist(filename: str) -> bool:
    file_path = os.path.join(VIDEOS_FOLDER, filename)
    return os.path.exists(file_path)


async def get_buffer(url: str) -> NamedTemporaryFile:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"{response.status_code} Could not fetch the video. Request denied by reddit.com"
        )
    return response.content


async def get_json(url: str) -> dict:
    json_url = url + ".json"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
    }
    response = requests.get(json_url, headers=headers)
    if response.status_code == 404:
        raise Exception("404 Post was not found.")
    if response.status_code != 200:
        raise Exception("Could not connect to reddit.com")
    return response.json()


def format_video_json(post_obj: dict) -> dict:
    try:
        post_data = post_obj[0]["data"]["children"][0]["data"]
    except:
        raise Exception("Could not read post json")

    if not post_data.get("is_video"):
        raise Exception("This post does not contain a video.")

    secure_media = post_data.get("secure_media")
    if not secure_media:
        raise Exception("This post does not provide secure video source.")

    video_info = secure_media["reddit_video"]
    video_url = video_info["fallback_url"]
    temp_url = "/".join(video_url.split("/")[:4])
    audio_url = temp_url + "/DASH_audio.mp4"

    video_obj = {
        "video_url": video_url,
        "audio_url": audio_url,
    }

    return video_obj


async def download_media(
    video_url: str, audio_url: str, filename: str = "reddit_video.mp4"
) -> str:
    video_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=TEMP_FOLDER)
    audio_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=TEMP_FOLDER)
    try:
        video_buffer, audio_buffer = await asyncio.gather(
            get_buffer(video_url), get_buffer(audio_url)
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
        raise e
    finally:
        video_file.close()
        os.unlink(video_file.name)
        audio_file.close()
        os.unlink(audio_file.name)


async def get_video_path(post_url: str) -> str:
    valid_url = valid_reddit_post(post_url)
    if not valid_url:
        raise Exception("Invalid reddit post url")

    filename = get_filename(post_url)
    video_exist = is_video_exist(filename)
    if video_exist:
        return filename

    post_json = await get_json(valid_url)
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
