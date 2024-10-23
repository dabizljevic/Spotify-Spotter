from flask import Flask, redirect, request, session, url_for, render_template_string
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os

#flask app and random secrete key creation.
app = Flask(__name__)
app.secret_key = os.urandom(12)

#spotify api credentials
CLIENT_ID = 'f26aee952fe54f308ae6743839a40d65'
CLIENT_SECRET = '6258e4f10ecc4fedb4470d38e9b10884'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

#scope for what we want to perform
SCOPE = "user-read-recently-played user-top-read"

#spotiftOAuth setup
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    redirect_uri=REDIRECT_URI, 
    scope=SCOPE
)

#homepage that redirects to the spotify login page
@app.route('/')
def home():
    return redirect(sp_oauth.get_authorize_url()) #redirect to spotify login using url

#callback for authentication response
@app.route('/callback')
def callback():
    try:
        #retrieve the authorization code from query 
        code = request.args.get('code')
        if not code:
            return "No code found in request. Please retry logging in.", 400

        #get and store token information
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info

        #check for expiration and update when necessary
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info

        #redirect to dashboard on login
        return redirect(url_for('dashboard'))

    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

#dashboard page with options for the user
@app.route('/dashboard')
def dashboard():
    #go back to homepage without working token
    if 'token_info' not in session:
        return redirect(url_for('home'))
    
    #quick html for dashboard
    dashboard_html = '''
    <h1>Spotify Dashboard</h1>
    <p>Choose an option below:</p>
    <ul>
        <li><a href="/recently-played">Recently Played Songs</a></li>
        <li><a href="/choose-time-range">Top Songs and Artists</a></li>
    </ul>
    '''
    
    #renders html
    return render_template_string(dashboard_html)

#shows recently played
@app.route('/recently-played')
def recently_played():
    try:
        #get token information and refresh if necessary
        token_info = session.get('token_info')
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info

        #create a spotift client to interact with
        sp = Spotify(auth=token_info['access_token'])

        #get last 50 song into list
        results = sp.current_user_recently_played(limit=50)
        tracks = [ #formatting here 
            item['track']['name'] + " by " + ", ".join(artist['name'] for artist in item['track']['artists'])
            for item in results['items']
        ]   

        #display songs
        return "<br>".join(tracks)
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

#page to choose time range for top artists and songs
@app.route('/choose-time-range')
def choose_time_range():
    #quick html for choices
    time_range_html = '''
    <h1>Select Time Range for Top Songs and Artists</h1>
    <ul>
        <li><a href="/top-songs-artists?time_range=short_term">Last 4 Weeks</a></li>
        <li><a href="/top-songs-artists?time_range=medium_term">Last 6 Months</a></li>
        <li><a href="/top-songs-artists?time_range=long_term">All Time</a></li>
    </ul>
    '''
    #render
    return render_template_string(time_range_html)

# route for top songs within a specified time
@app.route('/top-songs-artists')
def top_songs_artists():
    #get given time range 
    time_range = request.args.get('time_range', 'medium_term')  # default to 'medium_term'
    if time_range not in ['short_term', 'medium_term', 'long_term']:
        return "Invalid time range specified.", 400
    
    try:
        #get and handle current token 
        token_info = session.get('token_info')
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info

        sp = Spotify(auth=token_info['access_token'])

        #get top tracks artists for the time range
        top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_range)
        top_artists = sp.current_user_top_artists(limit=10, time_range=time_range)

        #formatting 
        top_songs = [
            "Top Songs (" + time_range.replace("_", " ").title() + "):<br>" + 
            "<br>".join([track['name'] + " by " + ", ".join(artist['name'] for artist in track['artists']) for track in top_tracks['items']])
        ]
        
        top_artists_list = [
            "Top Artists (" + time_range.replace("_", " ").title() + "):<br>" + 
            "<br>".join([artist['name'] for artist in top_artists['items']])
        ]

        #display
        return "<br><br>".join(top_songs + top_artists_list)
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

#run the app
if __name__ == '__main__':
    app.run(debug=True)
