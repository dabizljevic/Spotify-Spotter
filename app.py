from flask import Flask, redirect, render_template, request, session, url_for, render_template_string
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
@app.route('/')
def home():
    return render_template('index.html', is_authenticated='token_info' in session)
#homepage that redirects to the spotify login page
@app.route('/global')
def global_page():
    return render_template('global.html', is_authenticated='token_info' in session)

@app.route('/login_page')
def login_page():
    return render_template('login.html', is_authenticated='token_info' in session)

@app.route('/user')
def user_page():
    try:
        is_authenticated = 'token_info' in session
        # tracks = []
        #get token information and refresh if necessary
        if is_authenticated:
            token_info = session.get('token_info')
            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info

            #create a spotift client to interact with
            sp = Spotify(auth=token_info['access_token'])

            #get last 50 song into list
            results = sp.current_user_recently_played(limit=50)
            tracks = [ #formatting here 
                item['track']['name']  + " by " + ", ".join(artist['name'] for artist in item['track']['artists'])
                for item in results['items']
            ]
            return render_template('user.html', is_authenticated=is_authenticated, tracks=tracks, results = results['items']) 

        #display songs
        # return "<br>".join(tracks)
        return render_template('user.html')
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500
        

@app.route('/login')
def login():
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
    # if 'token_info' not in session:
    #     return redirect(url_for('home'))
    if 'token_info' not in session:
        return render_template('index.html')
    
    #quick html for dashboard
    # dashboard_html = '''
    # <h1>Spotify Dashboard</h1>
    # <p>Choose an option below:</p>
    # <ul>
    #     <li><a href="/recently-played">Recently Played Songs</a></li>
    #     <li><a href="/choose-time-range">Top Songs and Artists</a></li>
    # </ul>
    # '''
    
    # #renders html
    # return render_template_string(dashboard_html)
    return render_template('index.html', is_authenticated='token_info' in session)

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

#route for displaying user's top genres
@app.route('/top-genres')
def top_genres():
    try:
        #get token information and refresh if necessary
        token_info = session.get('token_info')
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info

        #create a Spotify client to interact with
        sp = Spotify(auth=token_info['access_token'])

        #get user's top artists to determine genres
        top_artists = sp.current_user_top_artists(limit=50)
        
        #gather genres from top artists and count occurrences
        genre_counts = {}
        for artist in top_artists['items']:
            for genre in artist['genres']:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        #sort genres by frequency
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        top_genres_list = [f"{genre}: {count}" for genre, count in sorted_genres[:10]]  # top 10 genres

        #display genres
        return "<br>".join(["Top Genres:"] + top_genres_list)
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

#route for displaying similar artists to user's favorite artists
@app.route('/similar-artists')
def similar_artists():
    try:
        #get token information and refresh if necessary
        token_info = session.get('token_info')
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info

        #create a Spotify client to interact with
        sp = Spotify(auth=token_info['access_token'])

        #get user's top artists and fetch similar artists for each
        top_artists = sp.current_user_top_artists(limit=10)  # limit for fewer API calls
        similar_artists_set = set()  # to avoid duplicates

        #iterate over user's top artists and get similar artists
        for artist in top_artists['items']:
            related_artists = sp.artist_related_artists(artist['id'])
            for related in related_artists['artists'][:3]:  # top 3 similar artists per artist
                similar_artists_set.add(related['name'])

        #display similar artists
        return "<br>".join(["Artists Similar to Your Favorites:"] + list(similar_artists_set))
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

#page for choosing the type of playlist
@app.route('/choose-playlist')
def choose_playlist():

    #playlist types listed
    playlist_options_html = '''
    <h1>Select Playlist Type</h1>
    <ul>
        <li><a href="/preview-playlist?type=top_tracks">Top Tracks Playlist</a></li>
        <li><a href="/preview-playlist?type=genre_based">Genre-Based Playlist</a></li>
        <li><a href="/preview-playlist?type=similar_artists">Similar Artists Playlist</a></li>
        <li><a href="/preview-playlist?type=mood_based">Mood-Based Playlist</a></li>
        <li><a href="/preview-playlist?type=recently_played">Recently Played Enhancer</a></li>
    </ul>
    '''

    return render_template_string(playlist_options_html)

#page to preview whatever playlist type was chosen
@app.route('/preview-playlist')
def preview_playlist():
    #get the type
    playlist_type = request.args.get('type')
    
    #contact spotify client
    token_info = session.get('token_info')
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info

    sp = Spotify(auth=token_info['access_token'])
    
    #generate the playlist based on chosen type
    if playlist_type == 'top_tracks':
        tracks = sp.current_user_top_tracks(limit=10)
        track_uris = [track['uri'] for track in tracks['items']]
        track_names = [f"{track['name']} by {track['artists'][0]['name']}" for track in tracks['items']]

    elif playlist_type == 'genre_based':
        top_artists = sp.current_user_top_artists(limit=50)
        genres = {genre for artist in top_artists['items'] for genre in artist['genres']}
        genre_tracks = []
        for genre in genres:
            results = sp.search(q=f'genre:"{genre}"', type='track', limit=2)
            genre_tracks.extend([track['uri'] for track in results['tracks']['items']])
        track_uris = genre_tracks[:10]
        track_names = [f"{sp.track(uri)['name']} by {sp.track(uri)['artists'][0]['name']}" for uri in track_uris]

    elif playlist_type == 'similar_artists':
        top_artists = sp.current_user_top_artists(limit=5)
        similar_artists_tracks = []
        for artist in top_artists['items']:
            related_artists = sp.artist_related_artists(artist['id'])
            for related in related_artists['artists'][:2]:
                results = sp.artist_top_tracks(related['id'])
                similar_artists_tracks.extend([track['uri'] for track in results['tracks'][:1]])
        track_uris = similar_artists_tracks[:10]
        track_names = [f"{sp.track(uri)['name']} by {sp.track(uri)['artists'][0]['name']}" for uri in track_uris]

    elif playlist_type == 'mood_based':
        top_tracks = sp.current_user_top_tracks(limit=10)
        mood_tracks = [track for track in top_tracks['items'] if sp.audio_features(track['uri'])[0]['valence'] > 0.5]
        track_uris = [track['uri'] for track in mood_tracks]
        track_names = [f"{track['name']} by {track['artists'][0]['name']}" for track in mood_tracks]

    elif playlist_type == 'recently_played':
        recent_tracks = sp.current_user_recently_played(limit=20)
        track_uris = [item['track']['uri'] for item in recent_tracks['items'][:10]]
        track_names = [f"{item['track']['name']} by {item['track']['artists'][0]['name']}" for item in recent_tracks['items'][:10]]

    else:
        return "Invalid playlist type selected.", 400

    #store track info and display
    session['track_uris'] = track_uris
    track_preview_html = '''
    <h1>Preview Playlist Tracks</h1>
    <ul>
    '''
    for track in track_names:
        track_preview_html += f"<li>{track}</li>"
    track_preview_html += '</ul><a href="/create-playlist">Add to Spotify</a>'
    return render_template_string(track_preview_html)

#creates playlist in spotify
@app.route('/create-playlist')
def create_playlist():
    try:
        #check if track URIs are in session
        track_uris = session.get('track_uris')
        if not track_uris:
            return "No tracks found. Please select a playlist type first.", 400
        
        #retrieve token and refresh if needed
        token_info = session.get('token_info')
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info

        sp = Spotify(auth=token_info['access_token'])
        
        #create a playlist in spotify and add tracks
        user_id = sp.current_user()['id']
        playlist_name = "Your Personalized Playlist"
        description = "A playlist created based on your listening habits"
        new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description=description)
        #add tracks to the playlist
        sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist['id'], tracks=track_uris) 

        return f"Playlist '{playlist_name}' created successfully!"

    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500
    

#run the app
if __name__ == '__main__':
    app.run(debug=True)
