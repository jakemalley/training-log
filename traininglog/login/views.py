# views.py
# Jake Malley
# 19/01/15

"""
Define the routes for the login blueprint.
"""

from flask import flash, redirect, render_template, request, \
                    url_for, Blueprint
from forms import LoginForm, SignUpForm

# Setup the login blueprint.
login_blueprint = Blueprint(
    'login',__name__,
    template_folder='templates'
    )

# Define the routes
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
            pass
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
            render_template('signup.html', user_signup_form=user_signup_form, error=error)

    return render_template('signup.html',user_signup_form=user_signup_form, error=error)