import json
from flask import Flask, redirect, request
from ThreefoldLoginPkg import ThreefoldLogin
from repo.ThreefoldLoginPkg.threefold_login import ThreefoldLogin
import string 
from urllib.parse import urlencode 
import random 


app = Flask(__name__)


def generate_authenticator():
    api_url = 'https://login.threefold.me'
    kyc_backend_url = 'https://openkyc.staging.jimber.org'

    email_identifier = 'omarabdul3ziz@gmail.com'
    seed_phrase = "dinner test old limit mass brief desk decline clarify scene strike accident olympic meadow click nuclear avocado outside share excite rookie snow adapt blast"
    
    app_id = '127.0.0.1:5000'
    redirect_url = "/callback"

    authenticator = ThreefoldLogin(api_url, app_id, seed_phrase, redirect_url, kyc_backend_url)

    allowed = string.ascii_letters + string.digits
    state = ''.join(random.SystemRandom().choice(allowed) for _ in range(32))
    login_url = authenticator.generate_login_url(state)

    callback_url = f"{app_id}{redirect_url}"

    return authenticator, state, login_url, callback_url, email_identifier

AUTHENTICATOR, STATE, LOGIN_URL, CALLBACK_URL, EMAIL_ID = generate_authenticator()

@app.route('/login')
def login():
    # DoneTODO: cause a http bad
    return redirect(LOGIN_URL)

@app.route('/callback')
def callback():
    #DoneTODO: get valid callback_url
    
    query = request.args.get("signedAttempt")
    params = urlencode({"signedAttempt": query})
    callback_url = f"http://{CALLBACK_URL}?{params}"

    authenticator = AUTHENTICATOR
    state = STATE
    email_id = EMAIL_ID

    msg = ""
    authenticator.parse_and_validate_redirect_url(callback_url, state)
    msg = 'successfully validated login attempt'

    resp = authenticator.verify_signed_email_idenfier(email_id)

    # if authenticator.is_email_verified(email_id):
    #     msg = msg + 'email is verified' 
    # else:
    #     msg = msg + 'email is not verified' 

    # try:
    #     msg = ""
    #     authenticator.parse_and_validate_redirect_url(callback_url, state)
    #     msg = 'successfully validated login attempt' 
    #     if authenticator.is_email_verified(email_id):
    #         msg = msg + 'email is verified' 
    #     else:
    #         msg = msg + 'email is not verified' 
    # except ValueError:
    #     msg = 'failed to validate login attempt' 

    return resp


if __name__=='__main__':
    app.run(debug=True)