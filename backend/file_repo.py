import json

users = None
games = None
next_game_id = 1

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

def create_game(player1):
    __read_games()
    global next_game_id
    game_id = next_game_id
    games[game_id] = {"player1":player1, "player2":None, "moves":[]}
    next_game_id += 1
    __write_games()
    return game_id

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

def __read_games():
    global games
    global next_game_id
    if games == None:
        try:
            with open("games.json") as f:
                games_and_id = json.loads(f.read())
                games = games_and_id["games"]
                next_game_id = games_and_id["next_id"]
        except:
            games = {}

def __write_games():
    with open("games.json", "w") as f:
        f.write(json.dumps({"games":games, "next_id":next_game_id}))
