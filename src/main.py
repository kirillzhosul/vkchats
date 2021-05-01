"""
    VK Peer Scaner (vk-peer-scaner)
    Description: Scans all your peers in VK, then sends it as message to you in VK.
"""

# Importing modulse
import vk_api.longpoll  # Module for working with VK API.
from vk_api.utils import get_random_id  # Module for getting random_id for sending a message.
from os import getenv  # Module for getting environment variable.


def api_send_message(peer_id, message):
    API_CONNECTION.method("messages.send", {
        "random_id": get_random_id(),
        "peer_id": peer_id,
        "message": message,
    })


def get_profile_id():
    return API_CONNECTION.method("account.getProfileInfo")["id"]


def format_peer_information(peer_info):
    print(f"Данные беседы {peer_info}")
    peer_title = peer_info["title"]
    peer_admin = "@id" + str(peer_info["admin_id"])
    peer_members = peer_info["members_count"]
    peer_id = peer_info["id"]
    peer_users = str(peer_info["users"])
    peer_kicked = peer_info["kicked"] if "kicked" in peer_info else 0
    return f"Title: {peer_title}, Admin: {peer_admin}, Members: {peer_members}, {'[KICKED]' if peer_kicked else '[ vk.com/im?sel=' + str(2000000000 + peer_id) + ' ]'}\n"  # Formatting.


def api_get_peer_data(peer_id):
    return API_CONNECTION.method("messages.getChat", {
        "random_id": get_random_id(),
        "chat_id": peer_id,
    })


if __name__ == "__main__":
    total_count = 0
    only_kicked = False
    API_TOKEN = "c9c698739db51483b4e03a61e47f258191a183ab53524dd292c7138bbba91074d4d016cb66ca3486d1a8f"  # Getting user token from environment variable.
    API_CONNECTION = vk_api.VkApi(token=API_TOKEN)
    API_LONGPOOL = vk_api.longpoll.VkLongPoll(API_CONNECTION)
    USER_ID = get_profile_id()
    api_send_message(USER_ID, "[PeerScaner] Scanning of the peers started.")
    current_peer_id = 0
    current_result = ""
    while True:
        current_peer_id += 1
        #try:
        peer_info = api_get_peer_data(current_peer_id)
        if "kicked" in peer_info:
            if bool(int(peer_info["kicked"])) and only_kicked:
                print("Kicked and passed.")
                continue
        current_result += format_peer_information(peer_info)
        total_count += 1
        print(total_count % 10)
        if total_count % 10 == 0:
            api_send_message(USER_ID, "[PeerScaner]: 10 Results:\n" + current_result)
            current_result = ""
        #except Exception as Error:
        #    if str(Error) == "[100] One of the parameters specified was missing or invalid: chat_id param is incorrect":
        #        break
        #    print(f"Ошибка {Error}")
    api_send_message(USER_ID, f"[PeerScaner] Scanning of the peers ended. (Total {total_count}")
