from logging import debug
from flask import Flask

from ThreefoldLoginPkg import ThreefoldLogin
import os
import string 
import random 

app = Flask(__name__)

# Init the authenticator
api_host = 'https://login.staging.jimber.org' # the login page
app_id = 'test'
seed_phrase = os.getenv("SEED_PHRASE")
callback_url = "/callback"
kyc_backend_url = 'https://openkyc.staging.jimber.org'
authenticator = ThreefoldLogin (api_host,
    app_id,
    seed_phrase,
    callback_url,
    kyc_backend_url
)

@app.route('/')
def home():
    admin = False
    if admin:
        return {'msg': "Hey admin"}
    else:
        return {'msg': "Hey Guest"}

@app.route('/protected')
def protected():
    return {'msg': "Hey admin"}

@app.route('/un_protected')
def un_protected():
    return {'msg': "Hey Guest"}

@app.route('/login')
def login():
    allowed = string.ascii_letters + string.digits
    state = ''.join(random.SystemRandom().choice(allowed) for _ in range(32))
    url = authenticator.generate_login_url(state)

    try:
        authenticator.parse_and_validate_redirect_url(callback_url, state)
        print('successfully validated login attempt')
        if authenticator.is_email_verified():
            print('email is verified')
        else:
            print('email is not verified')
    except ValueError:
        print('failed to validate login attempt')


@app.route('/logout')
def logout():
    pass

if __name__ == '__main__':
    app.run(debug=True)
