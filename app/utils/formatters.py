# Other modules
import xml.etree.ElementTree as ET

# App modules
from .errors import ServerError, BadRequest


def format_media_mdp(mpd_xml: str):
    root = ET.fromstring(mpd_xml)

    # Get the media presentation duration
    duration_str = root.attrib["mediaPresentationDuration"]
    duration = float(duration_str[2:-1])  # Extract the duration value as a float

    # Get the video representation information
    video_reprs = list()
    video_adaptation_set = root.find('.//AdaptationSet[@contentType="video"]')
    for repr_elem in video_adaptation_set.findall("Representation"):
        repr_info = {
            "id": repr_elem.attrib["id"],
            "width": int(repr_elem.attrib["width"]),
            "height": int(repr_elem.attrib["height"]),
            "bandwidth": int(repr_elem.attrib["bandwidth"]),
            "codecs": repr_elem.attrib["codecs"],
            "frame_rate": int(repr_elem.attrib["frameRate"]),
        }
        video_reprs.append(repr_info)

    # Get the audio representation information
    audio_reprs = list()
    audio_adaptation_set = root.find('.//AdaptationSet[@contentType="audio"]')
    for repr_elem in audio_adaptation_set.findall("Representation"):
        repr_info = {
            "id": repr_elem.attrib["id"],
            "bandwidth": int(repr_elem.attrib["bandwidth"]),
            "codecs": repr_elem.attrib["codecs"],
            "audio_sampling_rate": int(repr_elem.attrib["audioSamplingRate"]),
        }
        audio_reprs.append(repr_info)

    result = {
        "videos": video_reprs,
        "audios": audio_reprs,
        "duration": duration,
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
