# login/views.py
# Jake Malley
# 19/01/15

"""
Define the routes for the login blueprint.
"""

from flask import flash, redirect, render_template, request, \
                    url_for, Blueprint,abort
from forms import LoginForm, SignUpForm
from traininglog import bcrypt, app, db
from traininglog.models import Member
from flask.ext.login import login_user, logout_user, login_required
from datetime import datetime

# Setup the login blueprint.
login_blueprint = Blueprint(
    'login',__name__,
    template_folder='templates'
    )

# Define the routes.
@login_blueprint.route('/login', methods=['GET','POST'])
def login():
    """
    Renders the login.html template and displays it the user.
    """

    # Create an empty error variable.
    error = None

    # Create the login form.
    user_login_form = LoginForm()

    if request.method == 'POST':
        if user_login_form.validate_on_submit():
            # Do the user Login.
            # Query the database for a user that matches the email.
            member = Member.query.filter_by(email=user_login_form.email.data).first()
            if member is not None and bcrypt.check_password_hash(member.password,user_login_form.password.data):
                # The user is valid.
                # Log the In.
                login_user(member,remember=True)
                flash('Logged In')
                # Redirect them to the dashboard page.
                return redirect(url_for('dashboard.dashboard'))
            else:
                error='Invalid Credentials, Please try again.'
        else:
            render_template('login.html', user_login_form=user_login_form, error=error)


    return render_template('login.html',user_login_form=user_login_form, error=error)

@login_blueprint.route('/signup', methods=['GET','POST'])
def signup():
    """
    Renders the signup.html template and displays it to the user.
    """

    # Create an empty error variable.
    error = None

    # Create the sign up form.
    user_signup_form = SignUpForm()

    if request.method == 'POST':
        if user_signup_form.validate_on_submit():
            # Check the email isn't already in the database.
            member = Member.query.filter_by(email=user_signup_form.email.data).first()
            if member is None:
                # Not in the database, sign up the user.
                # Get the current time.
                now = datetime.utcnow()

                # Try and get the auto_aprove and auto_admin configuration.
                try:
                    if app.config['AUTO_ADMIN']:
                        is_admin = 1
                    else:
                        is_admin = 0
                except KeyError:
                    is_admin = 0

                try:
                    if app.config['AUTO_APROVE']:
                        is_active = 1
                    else:
                        is_active = 0
                except KeyError:
                    is_active = 0


                db.session.add(Member(user_signup_form.firstname.data, user_signup_form.surname.data, user_signup_form.email.data, user_signup_form.password.data, user_signup_form.gender.data, user_signup_form.height.data, user_signup_form.address_line_1.data,user_signup_form.city.data, user_signup_form.postcode.data,now,now,is_admin, is_active))

                db.session.commit()

                # Redirect them to the welcome page.(will change in future.)
                return redirect(url_for('home.welcome'))

            else:
                error = "An account is already associated with this email address."
        else:
            render_template('signup.html', user_signup_form=user_signup_form, user_login_form=LoginForm(), error=error)

    return render_template('signup.html', user_signup_form=user_signup_form, user_login_form=LoginForm(), error=error)

@login_blueprint.route('/logout')
@login_required
def logout():
    """
    Logs the current user out of the application.
    """
    logout_user()
    flash('You were logged out!')
    return redirect(url_for('home.welcome'))