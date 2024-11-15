import pytest
from app import app
from flask import session


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client


# test that accessing the /login route redirects to Spotify's authorization page
def test_login_redirects_to_spotify(client, monkeypatch):
    def mock_get_authorize_url():
        return "https://accounts.spotify.com/authorize?client_id=test_client_id"
    
    monkeypatch.setattr("app.sp_oauth.get_authorize_url", mock_get_authorize_url)

    response = client.get('/login')
    assert response.status_code == 302
    assert response.location.startswith("https://accounts.spotify.com/authorize")


# test the callback route without a code in the query string
def test_callback_no_code(client):
    response = client.get('/callback')
    assert response.status_code == 400
    assert b"No code found in request" in response.data


# test the callback route with a valid code to simulate authentication
def test_callback_with_code(monkeypatch, client):
    def mock_get_access_token(code):
        return {
            'access_token': 'mocked_access_token',
            'refresh_token': 'mocked_refresh_token',
            'expires_at': 9999999999
        }
    
    def mock_is_token_expired(token_info):
        return False

    monkeypatch.setattr('app.sp_oauth.get_access_token', mock_get_access_token)
    monkeypatch.setattr('app.sp_oauth.is_token_expired', mock_is_token_expired)

    response = client.get('/callback?code=mock_code')
    assert response.status_code == 302
    assert '/dashboard' in response.location

    with client.session_transaction() as sess:
        assert 'token_info' in sess
        assert sess['token_info']['access_token'] == 'mocked_access_token'


# test the /user route when authenticated
def test_user_page_authenticated(monkeypatch, client):
    # Mock Spotify API responses
    def mock_current_user_recently_played(*args, **kwargs):
        return {
            'items': [
                {
                    'track': {
                        'name': 'Mock Song 1',
                        'artists': [{'name': 'Mock Artist 1'}],
                        'album': {'images': [{'url': ''}, {'url': 'mock_image_url'}]}
                    }
                }
            ]
        }

    def mock_current_user_top_tracks(*args, **kwargs):
        return {
            'items': [
                {
                    'name': 'Top Track 1',
                    'artists': [{'name': 'Top Artist 1'}],
                    'album': {'images': [{'url': ''}, {'url': 'mock_track_image_url'}]}
                }
            ]
        }

    def mock_current_user_top_artists(*args, **kwargs):
        return {
            'items': [
                {'name': 'Top Artist 1', 'genres': ['rock'], 'images': [{'url': ''}, {'url': 'mock_artist_image_url'}]}
            ]
        }

    # Patch Spotify API methods to use mocks
    monkeypatch.setattr('app.Spotify.current_user_recently_played', mock_current_user_recently_played)
    monkeypatch.setattr('app.Spotify.current_user_top_tracks', mock_current_user_top_tracks)
    monkeypatch.setattr('app.Spotify.current_user_top_artists', mock_current_user_top_artists)

    # Set up session with valid token
    with client.session_transaction() as sess:
        sess['token_info'] = {
            'access_token': 'mocked_access_token',
            'refresh_token': 'mocked_refresh_token',
            'expires_at': 9999999999
        }

    # Test the /user route
    response = client.get('/user?time_range=short_term')
    assert response.status_code == 200
    #assert b"Mock Song 1" in response.data
    #assert b"Mock Artist 1" in response.data
    #assert b"mock_image_url" in response.data
    #assert b"Top Track 1" in response.data
    #assert b"Top Artist 1" in response.data
    #assert b"rock" in response.data



# test the similar artists route when authenticated
def test_similar_artists_page(monkeypatch, client):
    # Mock Spotify API responses
    def mock_current_user_top_artists(*args, **kwargs):
        return {'items': [{'id': 'mock_artist_id', 'name': 'Mock Top Artist'}]}

    def mock_artist_related_artists(artist_id):
        return {
            'artists': [
                {'name': 'Similar Artist 1', 'images': [{'url': ''}, {'url': 'similar_artist_image_url'}]},
                {'name': 'Similar Artist 2', 'images': [{'url': ''}, {'url': 'similar_artist_image_url_2'}]}
            ]
        }

    # Patch Spotify API methods to use mocks
    monkeypatch.setattr('app.Spotify.current_user_top_artists', mock_current_user_top_artists)
    monkeypatch.setattr('app.Spotify.artist_related_artists', mock_artist_related_artists)

    # Set up session with valid token
    with client.session_transaction() as sess:
        sess['token_info'] = {'access_token': 'mocked_access_token', 'expires_at': 9999999999}

    # Test the /similar-artists route
    response = client.get('/similar-artists')
    #assert response.status_code == 200
    #assert b"Similar Artist 1" in response.data
    #assert b"Similar Artist 2" in response.data
    #assert b"similar_artist_image_url" in response.data
    #assert b"similar_artist_image_url_2" in response.data

# test the listening history route with mocked data
def test_listening_history_page(monkeypatch, client):
    def mock_current_user_recently_played(*args, **kwargs):
        return {'items': [{'track': {'name': 'Listening History Song', 'artists': [{'name': 'History Artist'}], 'album': {'images': [{'url': ''}, {'url': 'mock_album_image_url'}]}}}]}

    monkeypatch.setattr('app.Spotify.current_user_recently_played', mock_current_user_recently_played)

    with client.session_transaction() as sess:
        sess['token_info'] = {'access_token': 'mocked_access_token', 'expires_at': 9999999999}

    response = client.get('/listening-history')
    assert response.status_code == 200
    assert b"Listening History Song" in response.data
    assert b"History Artist" in response.data
    assert b"mock_album_image_url" in response.data
