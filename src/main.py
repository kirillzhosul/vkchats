# Python VK chats scanner.
# Small script in the Python programming language,
# that scans and show you all your chats (conversations, peers) in the social network "Vkontakte".


# Importing modules.

# Other.
import vk_api
import vk_api.utils

# Preinstalled.
import os

# Settings.

# VK API Token (PATH, or token in or block).
VK_API_TOKEN = os.getenv("VK_USER_TOKEN") or "YOUR_TOKEN_HERE"
# USING OR STATEMENT MAY BE UNSAFE IF YOU ARE WANT TO CONTRIBUTE TO THIS PROJECT.
# PLEASE USE OS ENVIRONMENT TO SET YOUR USER TOKEN.

# Should exclude all where we kicked or left? (Overrides settings below).
EXCLUDE_NO_ACCESS = False

# Exclude left chats.
EXCLUDE_LEFT = False

# Exclude kicked chats.
EXCLUDE_KICKED = False

# Exclude joined chats.
EXCLUDE_JOINED = False

# In this mode there is only title, link, admin shown.
LINKS_MODE = False

# Send ALL values that you don't even need? (Photo, notifications is enabled,
VERBOSE = True

# Prefix for messages.
MESSAGE_PREFIX = "[VK Chats Scanner] "

# Chunk size (Change only if already used and know what is that).
CHUNK_SIZE = 10


# API Functions.

# VK API Method send message.
def vkapi_send_messages(_peer_index, _message, _prefix=MESSAGE_PREFIX):
    # Returning.
    return _vkapi_connection.method("messages.send", {
        "random_id": vk_api.utils.get_random_id(),
        "peer_id": _peer_index,
        "message": _prefix + _message
    })


# VK API Method get user id (of the token, to get peer with self).
def vkapi_get_user_id() -> int:
    # Returning.
    return _vkapi_connection.method("account.getProfileInfo")["id"]


# VK API Method that gets chat information.
def vkapi_get_chat(_chat_id) -> dict:
    # Returning.
    return _vkapi_connection.method("messages.getChat", {
        "chat_id": _chat_id
    })


# Function that parses chat, removes not used data and returns clean dict.
def parse_chat(_chat) -> dict:
    # Returning.
    return {
        "id": int(_chat["id"]),
        "title": str(_chat["title"]),
        "admin": int(_chat["admin_id"]),
        "members": int(_chat["members_count"]),
        "left": bool("left" in _chat),
        "kicked": bool("kicked" in _chat),
        "users": bool(_chat["users"]),
        "notifications": bool(_chat["push_settings"]["sound"] if "push_settings" in _chat else False),
        "photo": bool("is_default_photo" in _chat)
    }


# Function that formats link to the chat.
def chat_get_link(_chat_id) -> str:
    # Returning.
    return f"[vk.com/im?sel={2000000000 + _chat_id}]"


# Function that formats chat information.
def chat_format_information(_chat) -> str:
    # Excluding rules.
    _left = _chat["left"]
    _kicked = _chat["kicked"]
    if (_left and (EXCLUDE_LEFT or EXCLUDE_NO_ACCESS)) or \
            (_kicked and (EXCLUDE_KICKED or EXCLUDE_NO_ACCESS)) or \
                (not _left and not _kicked and EXCLUDE_JOINED):
        return ""
        
    # Getting chat title.
    _chat_title = _chat["title"]
    _chat_title = f"<{_chat_title}>"

    # Getting chat admin.
    _chat_admin = _chat["admin"]
    _chat_admin = f"[*id{_chat_admin} (Admin)]"

    # Getting members.
    _chat_members = _chat["members"]
    _chat_members = f"[{_chat_members}/50]" if _chat_members > 0 else ""

    # Getting chat state.
    _chat_state = "KICKED" if _chat["kicked"] else ("LEFT" if _chat["left"] else "JOINED")
    _chat_state = f"[{_chat_state}]"

    # Getting link.
    _chat_link = chat_get_link(_chat["id"])

    if VERBOSE:
        _chat_photo = _chat["photo"]
        _chat_photo = f"[Photo:{_chat_photo}]"
        _chat_notifications = _chat["notifications"]
        _chat_notifications = f"[Notifications:{_chat_notifications}]"
        _chat_users = _chat["users"]
        _chat_users = f"[Users:{_chat_users}]"

    # Returning.
    if LINKS_MODE:
        return " ".join([_chat_title, _chat_admin, _chat_link])
    else:
        if VERBOSE: 
             return " ".join([_chat_title, _chat_admin, _chat_members, _chat_state, _chat_link, _chat_photo, _chat_notifications, _chat_users])
        return " ".join([_chat_title, _chat_admin, _chat_members, _chat_state, _chat_link])


# Entry point function (Running script).
def run():
    # Getting profile peer.
    _profile_peer = vkapi_get_user_id()

    # Start message.
    vkapi_send_messages(_profile_peer, "Starting scanning chats...")

    # Already scanned count.
    _scanned_count = 0

    # Current chat_id for scanning.
    _current_chat_id = 1

    # Current chunk text.
    _current_chunk_chats = []

    # Shown count.
    _shown_count = 0

    while True:
        # Infinity loop.

        # Getting chat.
        try:
            # Getting.
            _chat = parse_chat(vkapi_get_chat(_current_chat_id))
        except vk_api.exceptions.ApiError:
            # If there is an error.

            # Breaking.
            break

        # Formatting chat.
        _chat = chat_format_information(_chat)

        # Adding chat to list.
        if _chat != "":
            _current_chunk_chats.append(_chat)
            _shown_count += 1

        # Printing debug.
        print(f"Processed chat with id {_current_chat_id}")

        # Increasing scanned count.
        _scanned_count += 1

        # Increasing current chat id.
        _current_chat_id += 1

        if len(_current_chunk_chats) != 0 and len(_current_chunk_chats) % CHUNK_SIZE == 0:
            # If this end of the chunk.

            # Sending chunk.
            vkapi_send_messages(_profile_peer, f"{CHUNK_SIZE} Chats:\n" +
                                ",\n".join(_current_chunk_chats))

            # Resetting chunk chats.
            _current_chunk_chats = []

    # Sending chunk.
    vkapi_send_messages(_profile_peer, f"{len(_current_chunk_chats)} Chats:\n" +
                        ",\n".join(_current_chunk_chats))

    # End message.
    vkapi_send_messages(_profile_peer, f"End scanning chats "
                                       f"(Total {_scanned_count} chats processed and {_shown_count} shown)...")


# Entry point.
if __name__ == "__main__":
    # If file itself.

    if VK_API_TOKEN == "YOUR_TOKEN_HERE":
        # If default token passed.

        # Debug message.
        print("You don't pass any access_token or os.getenv() not return any!")

        # Returning.
        exit(1)

    # Connecting to the VK API.
    try:
        # Trying to connect.

        # Connecting.
        _vkapi_connection = vk_api.VkApi(token=VK_API_TOKEN)
    except vk_api.exceptions.ApiError:
        # If there an error.

        # Error.
        print(f"Invalid access_token passed! Token: {VK_API_TOKEN}.")

    # Running entry point function.
    run()

raise SystemExit
