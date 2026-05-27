users = {}

OWNER_ID = 6590297265  # <-- твой Telegram ID

def set_user(user_id, level):
    users[user_id] = level

def get_user(user_id):
    return users.get(user_id, "FREE")

def is_owner(user_id):
    return user_id == OWNER_ID
