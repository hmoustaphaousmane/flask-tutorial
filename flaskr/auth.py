from flask import (
    flash, Blueprint, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # If the user submitted the form
    if request.method == 'POST':
        # Map submitted form keys and values (request.form) of username and pa
        username = request.form['username']
        password = request.form['password']

        db = get_db()  # Get a database connection
        error = None

        # Start validating the input (username and password)
        if not username:  # if the username is empty
            error = 'A username is required.'
        elif not username:  # if the password is empty
            error = 'A password is required.'

        if error is None:  # If the validation succeeds
            try:
                # Insert the username and the hashed password into (table) user
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()  # Save the changes
            except db.IntegrityError:
                # If the username already exist a db.IntegrityError will occur
                error = f"User {username} is already registered."
            else:
                # After registering a user, redirect to the login page
                return redirect(url_for('auth.login'))

        flash(error)  # Show the error to the user

    return render_template('auth/register.html')  # Render registration page
