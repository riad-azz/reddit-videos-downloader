# Flask modules
from flask import make_response

# Other modules
import json


def json_response(data: any, status_code: int = 200):
    json_str = json.dumps(data)
    response = make_response(json_str, status_code)
    response.headers["Content-Type"] = "application/json"
    return response
