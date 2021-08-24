import os
import requests

from urllib.parse import parse_qs

CLIENT_ID = os.getenv("GITHUB_ID")
CLIENT_SECRET = os.getenv("GITHUB_SECRET")
AUTHORIZATION_ENDPOINT = f"https://github.com/login/oauth/authorize?response_type=code&client_id={os.getenv('GITHUB_ID')}"
TOKEN_ENDPOINT = "https://github.com/login/oauth/access_token"
USER_ENDPOINT = "https://api.github.com/user"

# [1] send verification request 
print(f"Authorization URL: {AUTHORIZATION_ENDPOINT}")
# [2] back with auth code
code = input("Enter the code: ")

# [3] ask for access token by sending the oath code
res = requests.post(
    TOKEN_ENDPOINT,
    data=dict(
        client_id=os.getenv("GITHUB_ID"),
        client_secret=os.getenv("GITHUB_SECRET"),
        code=code,
    ),
)
# [4] response contain access token
res = parse_qs(res.content.decode("utf-8"))
token = res["access_token"][0]

# [5] obtain information from access token
user_data = requests.get(USER_ENDPOINT, headers=dict(Authorization=f"token {token}"))
username = user_data.json()["login"]
print(f"You are {username} on GitHub")

