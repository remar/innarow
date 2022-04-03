users = {}

def add_user(email):
    users[email] = email

def get_user(email):
    return users[email] if email in users else None
