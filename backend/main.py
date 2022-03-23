import os
import logging
from flask import Flask, request, session
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

gunicorn_logger = logging.getLogger('gunicorn.error')
if gunicorn_logger.handlers:
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route("/api/google-login", methods = ["POST"])
def google_login():
    token = request.data.decode("utf-8")
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
    app.logger.warning(token)
    app.logger.warning(idinfo)
    return "hejsan"
