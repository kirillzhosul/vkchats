"""
    VK Peer Scaner (vk-peer-scaner)
    Description: Scans all your peers in VK, then sends it as message to you in VK.
"""

# Importing modulse
import vk_api.longpoll  # Module for working with VK API.
from vk_api.utils import get_random_id  # Module for getting random_id for sending a message.
from os import getenv  # Module for getting environment variable.


def api_send_message(peer_id, message):
    """ Sends message using VK API. """
    API_CONNECTION.method("messages.send", {
        "random_id": get_random_id(),
        "peer_id": peer_id,
        "message": message,
    })


def get_profile_id():
    """ Gets profile id for current user. """
    return API_CONNECTION.method("account.getProfileInfo")["id"]


def format_peer_information(peer_info):
    """ Formats gived peer_info in message_format. """
    if DEBUG:
        # Debug mode.
        print(peer_info)
    # Getting data for the formatting.
    peer_title = peer_info["title"]  # Title.
    peer_admin = "@id" + str(peer_info["admin_id"])  # Admin id
    peer_members = peer_info["members_count"]  # Members count.
    peer_id = peer_info["id"]
    peer_users = str(peer_info["users"])
    peer_left = peer_info["left"]
    peer_kicked = peer_info["left"]
    # Formatting
    return f"Title: {peer_title}, Admin: {peer_admin}, Members: {peer_members}, {'[KICKED]' if peer_kicked else '[ vk.com/im?sel=' + str(2000000000 + peer_id) + ' ]'}\n"  # Formatting.


def api_get_peer_data(peer_id):
    """ Getting data for the gived peer_id and returning it. """
    return API_CONNECTION.method("messages.getChat", {
        "random_id": get_random_id(),
        "chat_id": peer_id,
    })


# Entry point.
if __name__ == "__main__":
    # Initialising variables.
    API_TOKEN = getenv("VK_USER_TOKEN")  # Getting user token from environment variable.
    API_CONNECTION = vk_api.VkApi(token=API_TOKEN)  # VK Connection.
    API_LONGPOOL = vk_api.longpoll.VkLongPoll(API_CONNECTION)  # VK Longpool.
    USER_ID = get_profile_id()  # User ID.
    # Settings.
    DEBUG = True  # If this is enabled, prints all data in console.
    # Starting scanning.
    api_send_message(USER_ID, "[PeerScaner] Scanning of the peers started.")
    current_peer_id = 0  # Current peer index for scanning
    current_result = ""  # Result as the string
    while True:
        # Endless loop.
        current_peer_id += 1  # Moving to the next peer.
        try:
            peer_info = api_get_peer_data(current_peer_id)  # Getting peer information.
            # Adding information to the result.
            current_result += format_peer_information(peer_info)
            if current_peer_id % 10 == 0:
                # If current peer id is 10 by count.
                # Sending result message to the user.
                api_send_message(USER_ID, "[PeerScaner]: 10 Results:\n" + current_result)
                # Clearing result.
                current_result = ""
        except Exception as Error:
            if str(Error) == "[100] One of the parameters specified was missing or invalid: chat_id param is incorrect":
                break  # Exiting loop if peers ended.
            if DEBUG:
                print(Error)  # DEBUG
    api_send_message(USER_ID, "[PeerScaner] Scanning of the peers ended.")  # Sending end message to the user.
