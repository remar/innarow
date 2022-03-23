import os
import logging
from flask import Flask, request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

gunicorn_logger = logging.getLogger('gunicorn.error')
if gunicorn_logger.handlers:
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route("/api/google-login", methods = ["POST"])
def google_login():
    app.logger.warning(request.data.decode("utf-8"))
    return "hejsan"
