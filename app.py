from flask import Flask, redirect, render_template, request, session, url_for, render_template_string
import spotipy
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
SCOPE = "user-read-recently-played user-top-read playlist-modify-public playlist-modify-private"

#cache handler setup
cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)

#spotiftOAuth setup
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    redirect_uri=REDIRECT_URI, 
    cache_handler=cache_handler,
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
        #get token information and refresh if necessary
        if is_authenticated:
            token_info = session.get('token_info')
            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info

            #create a spotift client to interact with
            sp = Spotify(auth=token_info['access_token'])

            #get last 50 song into list
            recent_tracks = sp.current_user_recently_played(limit=50)
            time_range = request.args.get('time_range', 'short_term')  # default to 'medium_term'
            if time_range not in ['short_term', 'medium_term', 'long_term']:
                return "Invalid time range specified.", 400
            restricted_top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_range)
            restricted_top_artists = sp.current_user_top_artists(limit=10, time_range=time_range)
            
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
            
            return render_template('user.html', is_authenticated=is_authenticated, recent_tracks = recent_tracks['items'], top_tracks = restricted_top_tracks['items'], top_artists = restricted_top_artists['items'], time_frame=time_range, top_genres=top_genres_list) 

        #display songs
        # return "<br>".join(tracks)
        return render_template('user.html')
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

@app.route('/listening-history')
def listening_history_page():
    try:
        is_authenticated = 'token_info' in session
        #get token information and refresh if necessary
        if is_authenticated:
            token_info = session.get('token_info')
            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info

            #create a spotift client to interact with
            sp = Spotify(auth=token_info['access_token'])

            recent_tracks = sp.current_user_recently_played(limit=50)

            return render_template('listening-history.html', is_authenticated=is_authenticated, recent_tracks=recent_tracks['items']) 

        return render_template('listening-history.html')
        #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

@app.route('/similar-artists')
def similar_artists_page():
    try:
        is_authenticated = 'token_info' in session
        #get token information and refresh if necessary
        if is_authenticated:
            token_info = session.get('token_info')
            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info

            #create a spotift client to interact with
            sp = Spotify(auth=token_info['access_token'])

            top_artists = sp.current_user_top_artists(limit=10)  # limit for fewer API calls
            similar_artists_set = set()  # to avoid duplicates

            #iterate over user's top artists and get similar artists
            for artist in top_artists['items']:
                related_artists = sp.artist_related_artists(artist['id'])
                for related in related_artists['artists'][:3]:  # top 3 similar artists per artist
                    tuple = (related['name'], related['images'][1]['url'])
                    similar_artists_set.add(tuple)

            #display similar artists
            # return "<br>".join(["Artists Similar to Your Favorites:"] + list(similar_artists_set))

            return render_template('similar-artists.html', is_authenticated=is_authenticated, similar = similar_artists_set) 

        #display songs
        # return "<br>".join(tracks)
        return render_template('similar-artists.html')
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

@app.route('/top-artists')
def top_artists_page():
    try:
        is_authenticated = 'token_info' in session
        #get token information and refresh if necessary
        if is_authenticated:
            token_info = session.get('token_info')
            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info

            #create a spotift client to interact with
            sp = Spotify(auth=token_info['access_token'])

            short_top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')
            medium_top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')
            long_top_artists = sp.current_user_top_artists(limit=10, time_range='long_term')
            
            return render_template('top-artists.html', is_authenticated=is_authenticated, short_term = short_top_artists['items'], medium_term = medium_top_artists['items'], long_term = long_top_artists['items']) 
        return render_template('top-artists.html')
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

@app.route('/top-songs')
def top_songs_page():
    try:
        is_authenticated = 'token_info' in session
        #get token information and refresh if necessary
        if is_authenticated:
            token_info = session.get('token_info')
            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info

            #create a spotift client to interact with
            sp = Spotify(auth=token_info['access_token'])

            short_top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
            medium_top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')
            long_top_tracks = sp.current_user_top_tracks(limit=10, time_range='long_term')

            return render_template('top-songs.html', is_authenticated=is_authenticated, short_term = short_top_tracks['items'], medium_term = medium_top_tracks['items'], long_term = long_top_tracks['items']) 

        return render_template('top-songs.html')
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

@app.route('/top-genres')
def top_genres_page():
    try:
        is_authenticated = 'token_info' in session
        #get token information and refresh if necessary
        if is_authenticated:
            token_info = session.get('token_info')
            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info

            #create a spotift client to interact with
            sp = Spotify(auth=token_info['access_token'])

            short_top_artists = sp.current_user_top_artists(limit=50, time_range='short_term')
            medium_top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')
            long_top_artists = sp.current_user_top_artists(limit=50, time_range='long_term')
        
            #gather genres from top artists and count occurrences
            short_genre_counts = {}
            for artist in short_top_artists['items']:
                for genre in artist['genres']:
                    short_genre_counts[genre] = short_genre_counts.get(genre, 0) + 1
            sorted_short_genres = sorted(short_genre_counts.items(), key=lambda x: x[1], reverse=True)
            short_top_genres_list = [f"{genre}: {count}" for genre, count in sorted_short_genres[:10]]  # top 10 genres

            medium_genre_counts = {}
            for artist in medium_top_artists['items']:
                for genre in artist['genres']:
                    medium_genre_counts[genre] = medium_genre_counts.get(genre, 0) + 1
            sorted_medium_genres = sorted(medium_genre_counts.items(), key=lambda x: x[1], reverse=True)
            medium_top_genres_list = [f"{genre}: {count}" for genre, count in sorted_medium_genres[:10]]  # top 10 genres

            long_genre_counts = {}
            for artist in long_top_artists['items']:
                for genre in artist['genres']:
                    long_genre_counts[genre] = long_genre_counts.get(genre, 0) + 1
            sorted_long_genres = sorted(long_genre_counts.items(), key=lambda x: x[1], reverse=True)
            long_top_genres_list = [f"{genre}: {count}" for genre, count in sorted_long_genres[:10]]  # top 10 genres

            
            
            return render_template('top-genres.html', is_authenticated=is_authenticated, short_term = short_top_genres_list, medium_term = medium_top_genres_list, long_term = long_top_genres_list) 
        return render_template('top-genres.html')
    
    #error handling
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Internal Server Error: {e}", 500

@app.route('/choose-playlist')
def choose_playlist_page():
    try:
        is_authenticated = 'token_info' in session
        #get token information and refresh if necessary
        if is_authenticated:
            token_info = session.get('token_info')
            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info
            
            #create a spotift client to interact with
            sp = Spotify(auth=token_info['access_token'])
    
            #generate the playlist based on chosen type
            # top_tracks = sp.current_user_top_tracks(limit=10)

            # top_track_uris = [track['uri'] for track in top_tracks['items']]

            # top_artists = sp.current_user_top_artists(limit=50)
            # genres = {genre for artist in top_artists['items'] for genre in artist['genres']}
            # genre_tracks = []
            # for genre in genres:
            #     results = sp.search(q=f'genre:"{genre}"', type='track', limit=2)
            #     genre_tracks.extend([track['uri'] for track in results['tracks']['items']])
            # genre_uris = genre_tracks[:10]      
                  
            # top_artists = sp.current_user_top_artists(limit=5)
            # similar_artists_tracks = []
            # for artist in top_artists['items']:
            #         related_artists = sp.artist_related_artists(artist['id'])
            #         for related in related_artists['artists'][:2]:
            #             results = sp.artist_top_tracks(related['id'])
            #             similar_artists_tracks.extend([track['uri'] for track in results['tracks'][:1]])
            # similar_artists_track_uris = similar_artists_tracks[:10]

            # mood_tracks = [track for track in top_tracks['items'] if sp.audio_features(track['uri'])[0]['valence'] > 0.5]
            # mood_track_uris = [track['uri'] for track in mood_tracks]
            
            # recent_tracks = sp.current_user_recently_played(limit=20)
            # recent_track_uris = [item['track']['uri'] for item in recent_tracks['items'][:10]]

            return render_template('choose-playlist.html', is_authenticated=is_authenticated) 
        return render_template('choose-playlist.html')
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
        token_info = sp_oauth.get_access_token(code, check_cache=False)
        print(f"Token info response: {token_info}")
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
