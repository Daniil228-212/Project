import json
import os
from datetime import datetime
DATA_FILE = "storage/betboom_cache.json"
def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"users": {}, "history": {}}, f)
def register_user(user_id, username):
    init_db()
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        if str(user_id) not in data["users"]:
            data["users"][str(user_id)] = {
                "username": username,
                "registration_date": datetime.now().isoformat(),
                "preferences": {}
            }
            f.seek(0)
            json.dump(data, f, indent=4)
            return True
    return False
def add_to_history(user_id, action, details):
    init_db()
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        history_id = len(data["history"]) + 1
        data["history"][str(history_id)] = {
            "user_id": str(user_id),
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        f.seek(0)
        json.dump(data, f, indent=4)
def get_user_history(user_id):
    init_db()
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return [item for item in data["history"].values() if item["user_id"] == str(user_id)]