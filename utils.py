import logging

from .api import (
    create_or_update_client,
    list_rooms,
    create_and_join_room,
    send_message,
    update_message,
)
from api.content.models import ProfileBrand

logger = logging.getLogger(__name__)


def get_or_create_chat_room(user_id, interlocutor_id):
    """Return id of chat room with 'interlocutor_id' if it exists,
    otherwise create and return created chat room id
    """

    user_token = ProfileBrand.objects.get(id=user_id).chattoken_set.latest(
        "expiration_date"
    )

    user_room_result = list_rooms(user_token.token)
    user_room_data = user_room_result["data"]
    # try find interlocutor id in rooms. if is exist, return room id
    for room in user_room_data:
        for member in room["members"]:
            if member["_id"] == interlocutor_id:
                return room["_id"]

    room_id = create_and_join_room(user_token.token, interlocutor_id)
    return room_id


def get_client_token(id_):
    """Return existed client token if it was saved in db
    or create new token
    """

    profile_brand = ProfileBrand.objects.get(id=id_)
    profile_brand_tokens = profile_brand.chattoken_set.all()
    if profile_brand_tokens:
        return profile_brand_tokens.latest("expiration_date").token

    token, expiration_date = create_or_update_client(id_)
    profile_brand.chattoken_set.create(token=token, expiration_date=expiration_date)

    return token


def send_giveaway_message(
    id_, chat_room_id, image, product_link, request_confirm_token
):
    """ Send message to 'chat_room_id' """

    message = "Hey, want to swap?"

    send_message(
        id_,
        chat_room_id,
        message,
        product_link,
        request_confirm_token,
        product_image=image,
    )


def update_giveaway_message(
    message_id, chat_room_id, image, update_request_status, client_id
):
    """
    Update sent giveaway request message

    update_request_status: 1 - accept, 0 - pending confirmation, -1 - decline
    """

    if update_request_status == 1:
        message = "Item passed on succesfully!\nCheck your WARDROBE."
    elif update_request_status == -1:
        message = "Item pass on declined."

    update_message(
        client_id,
        chat_room_id,
        message_id,
        message,
        update_request_status,
        product_image=image,
    )
