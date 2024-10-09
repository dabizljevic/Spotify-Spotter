from flask import Flask, redirect, request, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os

# Flask app creation
app = Flask(__name__)
app.secret_key = os.urandom(12)

# Spotify credentials
CLIENT_ID = 'f26aee952fe54f308ae6743839a40d65'  # from webpage
CLIENT_SECRET = '6258e4f10ecc4fedb4470d38e9b10884'  # from webpage
REDIRECT_URI = 'http://127.0.0.1:5000/callback'  # our URL

# Currently only reads recently played
SCOPE = "user-read-recently-played"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    redirect_uri=REDIRECT_URI, 
    scope=SCOPE
)

# Define a route for the homepage
@app.route('/')
def home():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Define a callback route to handle authentication response and display recent tracks
@app.route('/callback')
def callback():
    try:
        # Retrieve the authorization code from the URL
        code = request.args.get('code')
        
        if not code:
            return "No code found in request. Please retry logging in.", 400

        # Exchange authorization code for an access token
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info

        # Check if the token has expired, and refresh if needed
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info

        # Create a Spotify client with the access token
        sp = Spotify(auth=token_info['access_token'])

        # Get the user's last 50 recently played tracks
        results = sp.current_user_recently_played(limit=50)
        tracks = [
            item['track']['name'] + " by " + ", ".join(artist['name'] for artist in item['track']['artists'])
            for item in results['items']
        ]

        # Display the songs in the browser
        return "<br>".join(tracks)
    
    except Exception as e:
        # Print the error in the terminal and return it to the browser for debugging
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
