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
    # __name__: the name of the current Python module (import name)
    # The second argument tells the app that configuration files are relative
    # to the instance folder

    return app
