import json
from Game import Game

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
    games[str(game_id)] = {"player1":player1, "player2":None, "moves":[]}
    next_game_id += 1
    __write_games()
    return game_id

def get_games():
    __read_games()
    return list(games.keys())

def get_game(id):
    __read_games()
    if id not in games:
        return None
    return Game(
        games[id]["player1"],
        games[id]["player2"],
        games[id]["moves"],
        games[id]["winner"] if "winner" in games[id] else None
    )

def save_game(id, game):
    __read_games()
    games[id] = {"player1":game.player1, "player2":game.player2, "moves":game.moves, "winner":game.winner}
    __write_games()

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
