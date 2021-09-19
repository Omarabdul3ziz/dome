from flask import Flask, request, json, session, redirect
from beaker.middleware import SessionMiddleware
from urllib.parse import urlencode
from uuid import uuid4
import requests
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


# APIs URL
PROXY_OAUTH_SERVER_URL = "http://127.0.0.1:9000"
HOST_URL = 'https://login.threefold.me'

# App info
APP_ID = '127.0.0.1:5000'
REDIRECT_ROUTE = "/callback"

def generate_login_url():

    state = str(uuid4()).replace("-", "")
    session["state"] = state

    response = requests.get(f"{PROXY_OAUTH_SERVER_URL}/pubkey")
    response.raise_for_status() # will raise an HTTPError if the HTTP request returned an unsuccessful status code
    data = response.json()
    pubkey = data["publickey"].encode()

    params = {
        "state": state,
        "appid": APP_ID,
        "scope": json.dumps({"user": True, "email": True}),
        "redirecturl": REDIRECT_ROUTE,
        "publickey": pubkey,
    }

    url_params = urlencode(params)
    return f"{HOST_URL}?{url_params}"

@app.route("/login")
def login():
    return redirect(generate_login_url())

@app.route(REDIRECT_ROUTE)
def callback():
    state = session["state"]
    signed_attempt_val = request.args.get("signedAttempt")

    data = {
        "signedAttempt": signed_attempt_val,
        "state": state
    }

    response = requests.post(f"{PROXY_OAUTH_SERVER_URL}/verify", data=data)
    response.raise_for_status()

    return response.json()

# session_opts = {
#     'session.type': 'file',
#     "session.data_dir": "./data",
#     "session.auto": True
# }

# wsgi_app = SessionMiddleware(app, session_opts)

if __name__ == '__main__':
    app.run(debug=True)