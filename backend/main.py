import os
import logging
from flask import Flask, request, session, abort
from google.oauth2 import id_token
from google.auth.transport import requests
from functools import wraps
import file_repo as repo
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

gunicorn_logger = logging.getLogger('gunicorn.error')
if gunicorn_logger.handlers:
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "email" in session:
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper

@app.route("/api/google-login", methods = ["POST"])
def google_login():
    token = request.data.decode("utf-8")
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        app.logger.warning(token)
        app.logger.warning(idinfo)
        session["email"] = idinfo["email"]
        if not repo.get_user(idinfo["email"]):
            app.logger.warning(f"New user {idinfo['email']}!")
            repo.add_user(idinfo["email"])
        else:
            app.logger.warning("User exists!")
        return {}
    except ValueError:
        abort(401)

@app.route("/api/get-email", methods = ["GET"])
@login_required
def get_email():
    return session["email"]

@app.route("/api/users", methods = ["GET"])
@login_required
def get_users():
    return {"users":repo.get_users()}

@app.route("/api/games", methods = ["POST"])
@login_required
def create_game():
    game_id = repo.create_game(session["email"])
    return {}, 201, {"Location":f"/api/games/{game_id}"}

@app.route("/api/games", methods = ["GET"])
@login_required
def get_games():
    return {"games":repo.get_games()}

@app.route("/api/games/<int:id>", methods = ["GET"])
@login_required
def get_game(id):
    return repo.get_game(str(id)).to_json()

@app.route("/api/games/<int:id>", methods = ["PATCH"])
@login_required
def join_game(id):
    game = repo.get_game(str(id))
    if game.player2 == None:
        game.player2 = session["email"]
        repo.save_game(str(id), game)
        return {}, 200
    else:
        return {}, 409

@app.route("/api/games/<int:id>", methods=["POST"])
@login_required
def do_move(id):
    game = repo.get_game(str(id))
    if not game:
        return "Game not found", 404
    move = json.loads(request.data.decode())
    game.move(session["email"], int(move["x"]), int(move["y"]))
    repo.save_game(str(id), game)
    return {}, 200

# GET /api/users -> get all users -- why?
# GET /api/users/<id> -> get user with id -- why?
# POST /api/games -> create new game with user as first player
# GET /api/games -> list all games
# GET /api/games?status=open -> list games with only 1 player
# GET /api/games/<id> -> get game with id (any game? or just where you participate..?)
# PATCH /api/games/<id> -> join game
# POST /api/games/<id> {"X": 5, "Y": 3} OR? [5,3] -> put new piece on board
