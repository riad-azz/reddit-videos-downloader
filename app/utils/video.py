import os
import ffmpeg
import asyncio
import requests
from tempfile import NamedTemporaryFile
from flask import Flask, Response

app = Flask(__name__)


async def get_buffer(url: str) -> NamedTemporaryFile:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Could not fetch the video")
    return response.content


async def download():
    videoUrl = "https://v.redd.it/gnduh8gpiqra1/DASH_480.mp4?source=fallback"
    audioUrl = "https://v.redd.it/gnduh8gpiqra1/DASH_audio.mp4"

    video_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir="./temp")
    audio_file = NamedTemporaryFile(delete=False, suffix=".mp3", dir="./temp")
    output_file = NamedTemporaryFile(delete=False, suffix=".mp4", dir="./temp")
    try:
        video_buffer, audio_buffer = await asyncio.gather(
            get_buffer(videoUrl), get_buffer(audioUrl)
        )
        video_file.write(video_buffer)
        audio_file.write(audio_buffer)

        input_video = ffmpeg.input(video_file.name)
        input_audio = ffmpeg.input(audio_file.name)

        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(
            output_file.name, loglevel="quiet"
        ).run(overwrite_output=True, capture_stdout=False, capture_stderr=False)

        output_file.seek(0)
        output_buffer = output_file.read()

    except Exception as e:
        raise e
    finally:
        video_file.close()
        os.unlink(video_file.name)
        audio_file.close()
        os.unlink(audio_file.name)
        output_file.close()
        os.unlink(output_file.name)

    file_size = len(output_buffer)

    return Response(
        output_buffer,
        mimetype="video/mp4",
        headers={
            "Content-Length": file_size,
            "Content-Disposition": "attachment; filename=lol.mp4",
        },
    )
