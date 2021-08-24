import os
import requests
from flask import Flask, jsonify, redirect, url_for

from flask_dance.contrib.github import github, make_github_blueprint
from flask_login import logout_user, login_required, LoginManager

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # to make oath accept not https requests
GITHUB_ID = os.getenv("GITHUB_ID")
GITHUB_SECRET = os.getenv("GITHUB_SECRET")

app = Flask(__name__)

github_blueprint = make_github_blueprint(client_id=GITHUB_ID, client_secret=GITHUB_SECRET )
app.register_blueprint(github_blueprint)

app.config['SECRET_KEY'] = 'SUPER SECRET' # must to work

@app.route("/home")
def homepage():
    return jsonify(page="Home Page")

@app.route("/profile")
def profilepage():
    if not github.authorized:
        return redirect(url_for("homepage"))
    return jsonify(page="Profile Page")

@app.route("/login/github")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    res = github.get("/user")
    username = res.json()["login"]
    return f"You are @{username} on GitHub"

@app.route("/logout/github")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

if __name__ == "__main__":
    app.run(debug=True)