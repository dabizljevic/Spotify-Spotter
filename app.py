from flask import Flask, redirect, request, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os

#flask app creation
app = Flask(__name__)
app.secret_key = os.urandom(12)

#spotify credentials
CLIENT_ID = 'f26aee952fe54f308ae6743839a40d65'
CLIENT_SECRET = '6258e4f10ecc4fedb4470d38e9b10884'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

#currently only reads recently played
SCOPE = "user-read-recently-played"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

#define a route for the homepage
@app.route('/')
def home():
    # # creates spotify client
    # sp = spotipy.Spotify(auth=ACCESS_TOKEN)
    
    # # try's to get users last 50 songs
    # try:
    #     results = sp.current_user_recently_played(limit=50)
    #     tracks = [
    #         item['track']['name'] + " by " + ", ".join(artist['name'] for artist in item['track']['artists'])
    #         for item in results['items']
    #     ]

    #     # display songs
    #     return "<br>".join(tracks)
    # except spotipy.SpotifyException:
    #     return "Access token expired or invalid. Please regenerate a new one."
    return "<a href='/login'>Login with Spotify</a>"

# define a route for logging in
@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

#run
if __name__ == '__main__':
    app.run(debug=True)
