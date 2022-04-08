import json

users = None

def add_user(email):
    __read_users()
    users[email] = email
    __write_users()

def get_user(email):
    __read_users()
    return users[email] if email in users else None

def get_users():
    __read_users()
    return list(users.keys())

def __read_users():
    global users
    if users == None:
        try:
            with open("users.json") as f:
                users = json.loads(f.read())
        except:
            users = {}

def __write_users():
    with open("users.json", "w") as f:
        f.write(json.dumps(users))
