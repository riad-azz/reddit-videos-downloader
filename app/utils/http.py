# Other modules
import requests

# App modules
from .errors import ServerError, BadRequest

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
}


async def get_media_buffer(url: str) -> bytes:
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 404:
        raise BadRequest("404 Post media files not found.")
    if response.status_code != 200:
        raise ServerError(
            f"{response.status_code} Could not fetch the video. Request denied by reddit.com."
        )
    return response.content


async def get_post_mpd(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception("Could not connect to v.redd.it")

    return response.text


async def get_post_json(url: str) -> dict:
    json_url = url + ".json"
    response = requests.get(json_url, headers=HEADERS)
    if response.status_code != 200:
        raise ServerError("Could not connect to reddit.com.")

    if "application/json" not in response.headers.get("Content-Type", ""):
        raise BadRequest("404 Post was not found.")

    return response.json()
