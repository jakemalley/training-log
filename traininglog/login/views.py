# login/views.py
# Jake Malley
# 19/01/15

"""
Define the routes for the login blueprint.
"""

from flask import flash, redirect, render_template, request, \
                    url_for, Blueprint
from forms import LoginForm, SignUpForm
from traininglog import bcrypt
from traininglog.models import Member

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
                flash('Logged In')
                # Redirect them to the welcome page.(will change in future.)
                redirect(url_for('home.welcome'))
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
            # Do the user Login.
            pass
        else:
            render_template('signup.html', user_signup_form=user_signup_form, user_login_form=LoginForm(), error=error)

    return render_template('signup.html', user_signup_form=user_signup_form, user_login_form=LoginForm(), error=error)