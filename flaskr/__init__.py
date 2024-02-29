# This file will serve two purposes. First, it thells Python that the `flaskr`
# directory should be treated as a package. Second it will contain the app
# factory.

import os
from flask import Flask


def create_app(test_config=None):
    """
    Appliction factory function
    """

    # Create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    # __name__: the name of the current Python module (import name - root path)
    # The second argument tells the app that configuration files are relative
    # to the instance folder

    # Set some default configurations
    app.config.from_mapping(
        SECRET_KEY='dev',  # Used by Flask and extension to keep data safe
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')  # Path where
        # the SQLite database file will be saved
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)  # Override the
        # default configurations 👆 with values taken from the `config.py` file
        # in instance folder if it exists
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)  # Use test configuration instead
        # of instance configuration

    return app
