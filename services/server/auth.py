import os
from flask import jsonify, redirect, url_for
from flask_dance.contrib.github import github, make_github_blueprint

from app import app

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # to make oath accept not https requests
GITHUB_ID = os.getenv("GITHUB_ID")
GITHUB_SECRET = os.getenv("GITHUB_SECRET")

github_blueprint = make_github_blueprint(client_id=GITHUB_ID, client_secret=GITHUB_SECRET )
app.register_blueprint(github_blueprint, url_prefix="/login")


@app.route("/github")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    res = github.get("/user")
    username = res.json()["login"]
    assert res.ok
    return f"Welcom {username}"

def logged_in(func):
    def wrapper(*args, **kwargs):
        if not github.authorized:
            return redirect(url_for("github.login"))
        return func(*args, **kwargs)
    return wrapper

