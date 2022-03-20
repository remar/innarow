from flask import Flask, request

app = Flask(__name__)

@app.route("/api/google-login", methods = ["POST"])
def google_login():
    print(request.data.decode("utf-8"))
    return "hejsan"
