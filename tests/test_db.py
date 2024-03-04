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
