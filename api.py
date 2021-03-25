import logging

from .core import make_url, make_request, check_server_response


logger = logging.getLogger(__name__)


def create_or_update_client(id_: int) -> str:
    """ Update or create client id, bind token to client """

    url = make_url("admin", "clients")
    response = make_request(url, "POST", _id=id_, issueAccessToken=True)

    check_server_response(response)

    result = response.json()["result"]
    token = result["token"]
    expiration_date = result["expirationDate"]

    return token, expiration_date


def list_rooms(token: str) -> list:
    """ Return all user's rooms """

    url = make_url("rooms")
    response = make_request(url, "GET", client_token=token)

    check_server_response(response)

    result = response.json()["result"]
    return result


def create_and_join_room(token: str, invitee: int) -> int:
    """ Return created room id with 'invitee' user """

    url = make_url("rooms", "createAndJoin")
    response = make_request(
        url, "POST", client_token=token, invitee=invitee, roomType="direct"
    )

    check_server_response(response)

    result = response.json()["result"]
    return result["_id"]


def send_message(
    from_id: int,
    chat_room_id: int,
    message,
    product_link,
    request_confirm_token,
    message_type="spinRequest",
    product_image=None,
) -> None:
    """ Send mesage to chat 'chat_room_id' from user with id 'from_id' """

    url = make_url("messages")
    response = make_request(
        url,
        "POST",
        message=message,
        messageType=message_type,
        room=chat_room_id,
        sender=from_id,
        originalUrl=product_image,
        extra=(
            f'{{"productLink": "{product_link}",'
            f'"token": "{request_confirm_token}",'
            f'"requestConfirmStatus": "0"}}'
        ),
    )

    check_server_response(response)


def update_message(
    from_id: int,
    chat_room_id: int,
    message_id,
    message,
    update_request_status,
    message_type="spinRequest",
    product_image=None,
) -> None:
    """ Send mesage to chat 'chat_room_id' from user with id 'from_id' """

    url = make_url("messages")
    response = make_request(
        url,
        "POST",
        message=message,
        messageType=message_type,
        room=chat_room_id,
        sender=from_id,
        originalUrl=product_image,
        _id=message_id,
        extra=(f'{{"requestConfirmStatus":' f'"{update_request_status}"}}'),
    )

    check_server_response(response)
