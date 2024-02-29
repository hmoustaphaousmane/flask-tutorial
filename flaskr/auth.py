from flask import (
    flash, Blueprint, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# REGISTER VIEW
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


# LOGIN VIEW
@bp.route('/login', methods=('GET', 'POST'))
def login():
    # If the form is submitted
    if request.method == 'POST':
        # Map submitted form keys and values (request.form) of username and pa
        username = request.form['username']
        password = request.form['password']

        db = get_db()  # Get a database connection
        error = None

        # Query and store the user
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone  # Return one row from the query

        if user is None:  # If the user does not exists
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            # If the password is not valid (the submitted password is not
            # hashed in the same way as the stored hash)
            error = 'Incorrect password.'

        if error is None:
            session.clear()  # Clear the session
            session['user_id'] = user['id']  # Store user's id in the session
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# At the beginning of each request, if a user is logged in, load and make
# available their information to other views
@bp.before_app_request  # Register a function that runs before the view func
def load_logged_in_user():
    user_id = session.get('user_id')  # Get user's id from the session

    if user_id is None:  # If no user is registered in the session
        g.user = None
    else:  # Otherwise i.e. a user is stored in the session
        # Get the user's data from the database
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone  # g.user lasts for the length of the request


# LOGOUT VIEW
@bp.route('/logout')
def logout():
    session.clear()  # Clear the session (remove user's data from the session)
    return redirect(url_for('index'))
