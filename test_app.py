import pytest
from app import app
from flask import session



#function helps set up testing, making it easier to test our flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client



# test that the home page goes to the Spotify authentication URL
def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert 'https://accounts.spotify.com/authorize' in response.location

 # test the callback fails w no code in query string 
def test_callback_no_code(client):
    response = client.get('/callback')
    assert response.status_code == 400
    assert b"No code found in request" in response.data

#tests full run of app w mock spotify auth and tracks
def test_callback_with_code(monkeypatch, client):
    # mock function to return a mocked authorization URL
    def mock_get_authorize_url():
        return 'mocked_auth_url'

    # simulates getting an access token
    def mock_get_access_token(code):
        return {'access_token': 'mocked_access_token', 'refresh_token': 'mocked_refresh_token'}

    # simulates checking token expiration
    def mock_is_token_expired(token_info):
        return False

    # simulates refreshing the access token
    def mock_refresh_access_token(refresh_token):
        return {'access_token': 'refreshed_mocked_access_token'}

    # mocks retrieving recently played tracks
    def mock_current_user_recently_played(*args, **kwargs):
        return {
            'items': [
                {'track': {'name': 'Mock Song 1', 'artists': [{'name': 'Mock Artist 1'}]}},
                {'track': {'name': 'Mock Song 2', 'artists': [{'name': 'Mock Artist 2'}]}}
            ]
        }

    # patch into the app
    monkeypatch.setattr('app.sp_oauth.get_authorize_url', mock_get_authorize_url)
    monkeypatch.setattr('app.sp_oauth.get_access_token', mock_get_access_token)
    monkeypatch.setattr('app.sp_oauth.is_token_expired', mock_is_token_expired)
    monkeypatch.setattr('app.sp_oauth.refresh_access_token', mock_refresh_access_token)
    monkeypatch.setattr('app.Spotify.current_user_recently_played', mock_current_user_recently_played)

    # make request with mocked authorization code
    response = client.get('/callback?code=mock_code')

    # ensure the response and returned song are ok
    assert response.status_code == 200
    assert b"Mock Song 1 by Mock Artist 1" in response.data
    assert b"Mock Song 2 by Mock Artist 2" in response.data
