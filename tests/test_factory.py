from flaskr import create_app


# Test to check if the default configuration has testing set to False
def test_config():
    # Assert that the default app instance does not have testing set
    assert not create_app().testing
    # Assert that when TESTING is set in the app config, testing is indeed True
    assert create_app({'TESTING': True}).testing


# Test to check the /hello route endpoint
def test_hello(client):
    # Send a GET request to the /hello route using the client fixture
    response = client.get('/hello')
    # Assert that the response data matches the expected "Hello, World!"
    assert response.data == b'Hello, World!'
