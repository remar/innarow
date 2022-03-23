import os
import logging
from flask import Flask, request, session, abort
from google.oauth2 import id_token
from google.auth.transport import requests
from functools import wraps

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
        return {}
    except ValueError:
        abort(401)

@app.route("/api/get-email", methods = ["GET"])
@login_required
def get_email():
    return session["email"]
