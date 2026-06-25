import json
import os
import requests

USERNAMES = [
    "freddyfazbearcool091",
    "rar56705",
    "FalcoEve",
    "holabrandon2020",
    "Desne1207",
]

WEBHOOK_URL = "https://discord.com/api/webhooks/1519487370460926054/5qVBhAHuyANYrf3d_p_UPhnWjVGD00fVeGdp2jCPOJEqCjBht9xRcMTQDYiGG34Yxkf0"
STATE_FILE = "state.json"

PRESENCE_NAMES = {
    0: "Offline",
    1: "Online",
    2: "In Game",
    3: "In Studio",
}


def get_user_ids(usernames):
    resp = requests.post(
        "https://users.roblox.com/v1/usernames/users",
        json={"usernames": usernames, "excludeBannedUsers": True},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    return {entry["requestedUsername"]: entry["id"] for entry in data}


def get_presence(user_ids):
    resp = requests.post(
        "https://presence.roblox.com/v1/presence/users",
        json={"userIds": user_ids},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["userPresences"]


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def send_alert(username, presence_type, game_name=None):
    status = PRESENCE_NAMES.get(presence_type, "Unknown")
    description = f"**{username}** is now **{status}**"
    if game_name:
        description += f"\nPlaying: {game_name}"

    payload = {
        "embeds": [
            {
                "title": "Roblox Status Update",
                "description": description,
                "color": 0xC92A2A,
            }
        ]
    }
    r = requests.post(WEBHOOK_URL, json=payload, timeout=15)
    r.raise_for_status()


def main():
    name_to_id = get_user_ids(USERNAMES)
    if not name_to_id:
        print("No valid usernames resolved.")
        return

    id_to_name = {v: k for k, v in name_to_id.items()}
    presences = get_presence(list(name_to_id.values()))

    state = load_state()

    for p in presences:
        user_id = str(p["userId"])
        username = id_to_name.get(p["userId"], user_id)
        presence_type = p["userPresenceType"]
        game_name = p.get("lastLocation") if presence_type in (2, 3) else None

        prev_type = state.get(user_id, {}).get("presenceType", 0)

        # Only alert when going from offline/unknown -> online/in-game/in-studio
        if presence_type != 0 and presence_type != prev_type:
            send_alert(username, presence_type, game_name)
            print(f"Alert sent for {username}: {PRESENCE_NAMES.get(presence_type)}")
        elif presence_type == 0 and prev_type != 0:
            send_alert(username, 0)
            print(f"Alert sent for {username}: Offline")

        state[user_id] = {"presenceType": presence_type, "username": username}

    save_state(state)


if __name__ == "__main__":
    main()
