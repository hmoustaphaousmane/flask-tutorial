import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(  # Stablish a connection to the file pointed
            # by `DATABASE` config key
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Tell the connection to return rows
        # that behave like dicts. This allows accessing the coumns by name

    return g.db


def close_db(e=None):
    """Close a connection. Should be called after each request"""
    db = g.pop('db', None)

    # If the connection existes (g.db is set)
    if db is not None:
        db.close()  # Close it
