import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

# Open and read test data file
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()  # Create and open a temporary file

    app = create_app({
        'TESTING': True,  # Tell Flask the app is in test mode
        'DATABASE': db_path  # Override the database path so that it points
        # so it points to this temporary path instead of the instance folder
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)  # Execute test data script

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # Create and return a test client to make requests to the application
    # without running the server
    return app.test_client()


@pytest.fixture
def runner(app):
    # Create a runner that can call the Click commands registered with the app
    return app.test_cli_runner()
