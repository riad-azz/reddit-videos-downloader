# Other modules
import xmltodict

# App modules
from .errors import ServerError, BadRequest


def format_media_mpd(mpd_xml: str):
    mpd_dict = xmltodict.parse(mpd_xml)
    video_list = list()

    duration = float(mpd_dict["MPD"]["@mediaPresentationDuration"][2:-1])
    adaptation_sets = mpd_dict["MPD"]["Period"]["AdaptationSet"]

    audio_set = adaptation_sets[1]
    audio_repr = audio_set["Representation"]
    base_url = audio_repr["BaseURL"]
    bandwidth = int(audio_repr["@bandwidth"])
    sampling_rate = audio_repr["@audioSamplingRate"]
    audio_info = {
        "url": base_url,
        "bandwidth": bandwidth,
        "samplingRate": sampling_rate,
    }

    videos_set = adaptation_sets[0]
    for representation in videos_set["Representation"]:
        bandwidth = int(representation["@bandwidth"])
        height = int(representation["@height"])
        width = int(representation["@width"])
        base_url = representation["BaseURL"]
        video_info = {
            "url": base_url,
            "height": height,
            "width": width,
            "bandwidth": bandwidth,
        }
        video_list.append(video_info)

    result = {
        "duration": duration,
        "video": video_list,
        "audio": audio_info,
    }
    return result


def format_video_json(post_obj: dict) -> dict:
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

    video_info = secure_media["reddit_video"]
    if video_info.get("is_gif", ""):
        raise BadRequest("This post contains a gif not video.")

    video_url = video_info["fallback_url"]
    temp_url = "/".join(video_url.split("/")[:4])
    audio_url = temp_url + "/DASH_audio.mp4"

    video_obj = {
        "video_url": video_url,
        "audio_url": audio_url,
    }

    return video_obj
