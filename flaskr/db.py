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


def init_db():
    """Function that runs the script of schema.sql."""
    db = get_db()  # Get a database connection

    with current_app.open_resource('schema.sql') as f:  # Open the file schema
        db.executescript(f.read().decode('utf8'))  # Execute the commands read
        # from the file `scheman.sql`


# Define a new command line called `init-db` that calls the init_bd function
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initilized the database.')
