import logging
import requests
from json.decoder import JSONDecodeError
from typing import Dict

from django.conf import settings

from .exceptions import ImkitBackendResponseError


logger = logging.getLogger(__name__)


def get_request_metadata(response) -> Dict[str, str]:
    """ Get request metadata from Imkit backend response """

    return {
        "body": response.request.body,
        "headers": response.request.headers,
        "url": response.request.url,
        "method": response.request.method,
    }


def check_server_response(response) -> None:
    """ Check response from IMKIt server """

    json_response = None
    status_code = None

    try:
        json_response = response.json()
    except JSONDecodeError:
        exc_message = "Returned type of data not a json. Seems like request url wrong"
        raise ImkitBackendResponseError(exc_message, json_response)

    status_code = response.status_code

    if status_code == 401:
        metadata = get_request_metadata(response)
        exc_message = "Client api key or user authorization key wrong"
        raise ImkitBackendResponseError(exc_message, json_response, metadata=metadata)
    elif status_code != 200:
        metadata = get_request_metadata(response)
        exc_message = "Server returned not 200 status code"
        raise ImkitBackendResponseError(exc_message, json_response, metadata=metadata)


def make_request(url: str, method: str, client_token=None, **kwargs):
    """ Make request to imkit chat backend. Pass '**kwargs' to body of request """

    if client_token is None:
        headers = {"API_KEY": settings.IMKIT_API_KEY}
    else:
        headers = {
            "CLIENT_KEY": settings.IMKIT_CLIENT_KEY,
            "Authorization": client_token,
        }

    return requests.request(method=method, url=url, headers=headers, data=kwargs)


def make_url(*args) -> str:
    """
    Build url for making request to imkit chat backend. Add access token
    to header

    """

    url = f"{settings.IMKIT_CHAT_SERVER_URL}/{'/'.join(args)}"

    return url
