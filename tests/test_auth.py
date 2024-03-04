import pytest
from flaskr import g, session
from flaskr.db import get_db


def test_register(client, app):
    # Asser that the page renders successfully by making a get request
    # (client.get makes a GET request and returns the Response object returned
    # by Flask) and check for a 200 OK status code
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["location"] == '/auth/login'
    # headers will have a Location header with the login URL when the register
    # view redirects to the login view

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is None


# Tell Pytest to run the same test function with different arguments thanks to
# `pytest.mark.parametrize`
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
    # data contains the body of the response as bytes


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
