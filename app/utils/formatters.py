# Other modules
import re
import xmltodict

# App modules
from .errors import ServerError, BadRequest

DOWNLOAD_ROUTE = "/ajax/download"


def bandwidth_to_size(bandwidth: int, duration: float) -> float:
    size = (bandwidth / 8) * duration
    return size / 1048576


def sanitize_text(text: str) -> str:
    return re.sub(r"[^\w\s-]", "", text)


def format_post_json(post_obj: dict) -> dict:
    try:
        post_data = post_obj[0]["data"]["children"][0]["data"]
    except:
        raise ServerError("Could not read the post json.")

    if post_data.get("removed_by_category", "") == "deleted":
        raise BadRequest("Yikes! looks like this post was deleted.")

    if not post_data.get("is_video"):
        raise BadRequest("This post does not contain a video.")

    secure_media = post_data.get("secure_media")
    if not secure_media:
        raise BadRequest("This post does not provide secure video source.")

    video_info = secure_media.get("reddit_video")
    if not video_info:
        raise BadRequest("This post does not host a reddit video.")

    if video_info.get("is_gif", ""):
        raise BadRequest("This post contains a gif not video.")

    title = post_data["title"]
    sanitized_title = sanitize_text(title)
    duration = int(video_info["duration"])
    url = post_data["url"]
    dash_url = video_info["dash_url"]

    post_json = {
        "title": sanitized_title,
        "duration": duration,
        "url": url,
        "dash_url": dash_url,
    }

    return post_json


def format_mpd(mpd_xml: str, post_url: str):
    mpd_dict = xmltodict.parse(mpd_xml)

    adaptation_sets = mpd_dict["MPD"]["Period"]["AdaptationSet"]

    try:
        audio_set = adaptation_sets[1]
        audio_repr = audio_set["Representation"]
        audio_url = post_url + "/" + audio_repr["BaseURL"]
        audio_bandwidth = int(audio_repr["@bandwidth"])
        audio_sampling_rate = audio_repr["@audioSamplingRate"]
        audio_info = {
            "url": audio_url,
            "bandwidth": audio_bandwidth,
            "samplingRate": audio_sampling_rate,
        }
    except:
        raise ServerError("No audio found for this post")

    video_list = list()
    try:
        videos_set = adaptation_sets[0]
        for representation in videos_set["Representation"]:
            video_url = post_url + "/" + representation["BaseURL"]
            video_height = representation["@height"]
            video_width = representation["@width"]
            video_bandwidth = int(representation["@bandwidth"])
            video_info = {
                "url": video_url,
                "height": video_height,
                "width": video_width,
                "bandwidth": video_bandwidth,
            }
            video_list.append(video_info)
    except:
        raise ServerError("Could not fetch video info for this post")

    result = {
        "videos": video_list,
        "audio": audio_info,
    }
    return result


def format_video_info(title: str, duration: int, mpd_json: dict) -> dict:
    video_info = dict

    audio_url = mpd_json["audio"]["url"]

    videos = list()
    for video in mpd_json["videos"]:
        video_url = video["url"]
        quality = video["height"] + "p"
        download_url = (
            f"{DOWNLOAD_ROUTE}?title={title}&video={video_url}&audio={audio_url}"
        )
        video_obj = {
            "quality": quality,
            "url": download_url,
        }
        videos.append(video_obj)

    video_info = {
        "title": title,
        "duration": duration,
        "options": videos,
    }

    return video_info
