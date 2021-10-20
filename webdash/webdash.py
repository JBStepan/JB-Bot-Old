"""
Example of using Discord OAuth to allow someone to
log in to your site. The scope of 'email+identify' only
lets you see their email address and basic user id.
"""
from datetime import time
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, make_response, render_template
import os
import json

# Disable SSL requirement
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Settings for your app
base_discord_api_url = 'https://discordapp.com/api'
client_id = r'790729528837537812' # Get from https://discordapp.com/developers/applications
client_secret = ''
redirect_uri='http://127.0.0.1:5000/oauth_callback'
scope = ['identify', 'email', 'guilds']
token_url = 'https://discordapp.com/api/oauth2/token'
authorize_url = 'https://discordapp.com/api/oauth2/authorize'
users_json = u"C:/Users/wayne/Desktop/Jakob2/JB Programs/data/jb-bot/users.json"

logged_in = False

app = Flask(__name__)
app.secret_key = os.urandom(24)

class Econ:
    def __init__(self, wallet, bank, items) -> None:
        self.wallet = wallet
        self.bank = bank
        self.items = items

def get_bank_data(id):
    with open(users_json, 'r') as f:
        users = json.load(f)
    
    wallet = users[str(id)]["econ-wallet"]
    bank = users[str(id)]["econ-bank"]
    items = users[str(id)]["econ-items"]

    return Econ(wallet, bank, items)

def bot_web_login(id, avatar_url):
    with open(users_json, 'r') as f:
        users = json.load(f)
    
    if users[str(id)] in users:
        users[str(id)]["weblogin"] = True
        users[str(id)]["avatar-url"] = avatar_url

        with open(users_json, 'w') as f:
            json.dump(users, f, indent=4)
        
        return True
    else:
        return False

def has_web_login(id):
    with open(users_json, 'r') as f:
        users = json.load(f)
    
    if users[str(id)] in users:
        if users[str(id)]["weblogin"] == True:
            return [0]
        else:
            return [1]
    else:
        return [3]

@app.route("/")
def home():
    global logged_in

    """
    Presents the 'Login with Discord' link
    """

    if logged_in == True:
        return render_template("index.html", logged_in=True, login_url=None)
    else:
        return '<a href="' + url_for("login") + '">Login with Discord</a>'
    
@app.route("/login")
def login():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session['state'] = state
    print(login_url)
    return redirect(login_url)

@app.route("/oauth_callback")
def oauth_callback():
    global logged_in
    """
    The callback we specified in our app.
    Processes the code given to us by Discord and sends it back
    to Discord requesting a temporary access token so we can 
    make requests on behalf (as if we were) the user.
    e.g. https://discordapp.com/api/users/@me
    The token is stored in a session variable, so it can
    be reused across separate web requests.
    """
    discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'], scope=scope)
    token = discord.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url,
    )
    session['discord_token'] = token
    logged_in = True
    resp = make_response(redirect(url_for("my_profile")))
    return resp

@app.route('/has_web_login/')
def has_weblogin():
    d = OAuth2Session(client_id, token=session['discord_token'])
    r = d.get(base_discord_api_url + '/users/@me')

    id = request.args.get('id')

    if has_web_login(id) == [0]:
        pass

@app.route("/my_profile")
def my_profile():
    global logged_in

    """
    Example profile page to demonstrate how to pull the user information
    once we have a valid access token after all OAuth negotiation.
    """
    if logged_in == True:
        discord = OAuth2Session(client_id, token=session['discord_token'])
        response = discord.get(base_discord_api_url + '/users/@me')
        # https://discordapp.com/developers/docs/resources/user#user-object-user-structure
        avatar = f"https://cdn.discordapp.com/avatars/{response.json()['id']}/{response.json()['avatar']}.png"
        return render_template('profile.html', username=response.json()['username'], 
        wallet_amount=get_bank_data(response.json()['id']).wallet, 
        bank_amount=get_bank_data(response.json()['id']).bank, 
        avatar=avatar)
    else:
        return redirect(url_for('login'))

@app.route("/profile/")
def profile():
    id = request.args.get('id')
    print(id)
    return f"{id}"

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
