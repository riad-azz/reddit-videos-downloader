# Other modules
import io
import os
import shutil
import ffmpeg
import asyncio
from tempfile import NamedTemporaryFile

# App modules
from app import BASE_DIR
from .http import get_media_bytes, get_post_json, get_post_mpd
from .formatters import format_post_json, format_mpd, format_video_info
from .validators import validate_post_url
from .errors import ServerError, HTTPException

TEMP_FOLDER = BASE_DIR / "media/temp"


async def download_video(video_url: str, audio_url: str, folder_name: str) -> str:
    output_folder = TEMP_FOLDER / folder_name
    os.makedirs(output_folder)

    video_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=output_folder)
    audio_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=output_folder)
    output_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir=output_folder)
    try:
        video_buffer, audio_buffer = await asyncio.gather(
            get_media_bytes(video_url),
            get_media_bytes(audio_url),
        )
        video_file.write(video_buffer)
        audio_file.write(audio_buffer)

        input_video = ffmpeg.input(video_file.name)
        input_audio = ffmpeg.input(audio_file.name)

        # run ffmpeg asynchronously
        process = (
            ffmpeg.concat(input_video, input_audio, v=1, a=1)
            .output(output_file.name, loglevel="quiet", preset="medium", crf=23)
            .run_async(overwrite_output=True)
        )

        # wait for process to finish
        process.wait()

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
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)


async def get_video_list(post_url: str) -> dict:
    valid_url = validate_post_url(post_url)

    post_json = await get_post_json(valid_url)
    post_json = format_post_json(post_json)
    title = post_json["title"]
    duration = post_json["duration"]
    url = post_json["url"]
    dash_url = post_json["dash_url"]

    post_mpd = await get_post_mpd(dash_url)
    mpd_json = format_mpd(post_mpd, url)

    video_info = format_video_info(title, duration, mpd_json)
    return video_info


async def get_video(post_url: str) -> dict:
    valid_url = validate_post_url(post_url)

    post_json = await get_post_json(valid_url)
    post_json = format_post_json(post_json)
    title = post_json["title"]
    video_url = post_json["video_url"]
    audio_url = post_json["audio_url"]
    download_url = f"/ajax/download?title={title}&video={video_url}&audio={audio_url}"

    video = {
        "title": title,
        "download_url": download_url,
    }
    return video
