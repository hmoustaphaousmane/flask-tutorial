import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        # Assert that get_db() returns the same connectin each time it's called
        assert db is get_db()

    # Try executing a query after the context exits, which should raise an err
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    # Assert that the raised error indicates a closed connection
    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """
    Ensure that `init-db` command calls  the `init_db` function
    """

    class Recorder(object):
        """
        Helper class to track if `init_db` is called without executing it
        """
        called = False

    def fake_init_db():
        """
        Mock implementation of `init_db` that sets `Recorder.called` to True
        """
        Recorder.called = True

    # Monkeypatch the actual init_db function with the fake implementation
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)  # i.e. replace the
    # init_db function with one that records that it’s been called

    # Invoke the 'init-db' command using the test runner
    result = runner.invoke(args=['init-db'])

    # Assert successful initialization
    assert 'Initialized' in result.output
    # Assert that The init_db function should have been called
    assert Recorder.called
