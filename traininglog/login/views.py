# login/views.py
# Jake Malley
# 19/01/15

"""
Define the routes for the login blueprint.
"""

from flask import flash, redirect, render_template, request, \
                    url_for, Blueprint
from forms import LoginForm, SignUpForm, EditDetailsForm, ChangePasswordForm
from traininglog import bcrypt, app, db
from traininglog.models import Member,Exercise
from flask.ext.login import login_user, logout_user, login_required, current_user, fresh_login_required
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
        # If the form was submitted. (i.e. data posted to the page.)
        if user_login_form.validate_on_submit():
            # Do the user Login.
            # Query the database for a user that matches the email.
            member = Member.query.filter_by(email=user_login_form.email.data).first()
            if member is not None and bcrypt.check_password_hash(member.password,user_login_form.password.data):
                # The user is valid.
                # Log the In.
                if login_user(member,remember=bool(user_login_form.remember.data)):
                    # All is okay log the user in.
                    flash('Logged In')
                    # Update the last login date.
                    member.set_last_login_date(datetime.utcnow())
                    # Commit changes to the database.
                    db.session.commit()
                    # If the user was trying to access a page before he was redirected here
                    # redirect them back to that page.
                    if request.args.get('next'):
                        return redirect(request.args.get('next'))
                    else:
                        # Redirect them to the dashboard page.
                        return redirect(url_for('dashboard.dashboard'))
                else:
                    # The user cannot be logged in.
                    if not member.is_active():
                        # The account is not activated as account_is_active returns False
                        error = "Account is not active, please contact your system administrator."
                    else:
                        # Unknown error.
                        error = "Unknown error occurred, please contact your system administrator."
            else:
                # Either the user does not exist or the password doesn't match.
                # Error message left vague for security.
                error="Invalid Credentials, Please try again."
    # Display the login.html page to the user.
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
                    if app.config['AUTO_APPROVE']:
                        is_active = 1
                    else:
                        is_active = 0
                except KeyError:
                    is_active = 0

                member = Member(user_signup_form.firstname.data, user_signup_form.surname.data, user_signup_form.email.data, user_signup_form.password.data, user_signup_form.gender.data, user_signup_form.height.data, user_signup_form.address_line_1.data,user_signup_form.city.data, user_signup_form.postcode.data,now,now,is_admin, is_active)

                db.session.add(member)
                db.session.commit()

                # Redirect them to the dashboard. (Also log them in.)
                if login_user(member):
                    # All is okay log the user in.
                    flash('Logged In')
                    # Redirect them to the dashboard page.
                    return redirect(url_for('dashboard.dashboard'))
                else:
                    # For some reason the user could not be logged in.
                    if not member.is_active():
                        # The account is not activated as account_is_active returns False (AUTO_APPROVE set to False)
                        error = "Before you can login the system requires an administrator approves your account."
                    else:
                        # Redirect them to the login page. The error will be dealt with there.
                        return redirect(url_for('login.login'))
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

@login_blueprint.route('/myprofile', methods=['GET','POST'])
@fresh_login_required
def myprofile():
    """
    Displays the profile of the current user.
    """

    # Create an empty error variable.
    error = None

    # Create the edit details form.
    user_edit_details_form = EditDetailsForm()

    if request.method == 'POST':
        if user_edit_details_form.validate_on_submit():
            # The form is valid. I.e all the data require is there.
            # Check the password matches the users password.
            if bcrypt.check_password_hash(current_user.password,user_edit_details_form.password.data):
                # Okay that is the correct password make the changes.
                current_user.update_details(user_edit_details_form.firstname.data, user_edit_details_form.surname.data, user_edit_details_form.email.data, user_edit_details_form.height.data, user_edit_details_form.address_line_1.data, user_edit_details_form.city.data, user_edit_details_form.postcode.data)
                # Commit the changes.
                db.session.commit()
                flash("Successfully updated your personal details.")
            else:
                error = "Incorrect Password, changes have not been made."
        else:
            render_template('myprofile.html',error=error, user_edit_details_form=user_edit_details_form, user_change_password_form=ChangePasswordForm())
    return render_template('myprofile.html',error=error, user_edit_details_form=user_edit_details_form, user_change_password_form=ChangePasswordForm())

@login_blueprint.route('/chgpasswd', methods=['POST','GET'])
@fresh_login_required
def chgpasswd():
    """
    Changes the users password.

    The only available method is POST as the form is on the 'myprofile' page. This 
    route just validates the form. If the method is GET the user is redirected to the
    'myprofile' page.
    """

    if request.method == 'GET':
        return redirect(url_for('login.myprofile'))

     # Create an empty error variable.
    error = None

    # Create the change password form.
    user_change_password_form = ChangePasswordForm()

    if user_change_password_form.validate_on_submit():
        # The form is valid.
        # Check the current password is correct.
        if bcrypt.check_password_hash(current_user.password,user_change_password_form.current_password.data):
            # If the current password matched update the new password.
            current_user.update_password(user_change_password_form.new_password.data)
            # Commit the changes to the database.
            db.session.commit()
            # Flash a message to the user.
            flash("Password has been successfully changed.")
        else:
            flash("Invalid password password has not been changed",'error')
    
    return render_template('myprofile.html',error=error, user_edit_details_form=EditDetailsForm(), user_change_password_form=user_change_password_form)

@login_blueprint.route('/deleteaccount', methods=['POST','GET'])
@fresh_login_required
def delete_account():
    """
    Deletes the current users account.
    """
    
    # If the got here by GET redirect them.
    if request.method == 'GET':
        flash("Invalid URL.",'error')
        return redirect(url_for('login.myprofile'))

    # Make sure the password was correct
    if bcrypt.check_password_hash(current_user.password,request.form['password']) and request.form['delete_account'] == 'True':
        # Delete the users account.
        # Get their exercise data. 
        exercise_data = Exercise.query.filter_by(member=current_user).all()
        # For each piece of data.
        for data in exercise_data:
            # Delete the data.
            db.session.delete(data)

        # Finally delete the user.
        db.session.delete(current_user)
        # Make sure that user has been logged out.
        logout_user()
        # Commit the changes.
        db.session.commit()
        # Flash a message.
        flash('Account has been delete!')
        # Redirect to the welcome page.
        return redirect(url_for('home.welcome'))
        
    else:
        flash("Invalid password account has not been deleted.",'error')

    return redirect(url_for('login.myprofile'))

@login_blueprint.route('/deactivateaccount', methods=['POST','GET'])
@fresh_login_required
def deactivate_account():
    """
    Deactivates the current users account.
    """
    # If the got here by GET redirect them.
    if request.method == 'GET':
        flash("Invalid URL.",'error')
        return redirect(url_for('login.myprofile'))

    # Make sure the password was correct
    if bcrypt.check_password_hash(current_user.password,request.form['password']) and request.form['deactivate_account'] == 'True':
        # Deactivate the users account.
        current_user.account_is_active = 0
        # Commit the changes.
        db.session.commit()
        # Logout the user.
        logout_user()
        # Flash a message.
        flash("Account has been deactivated!")
        # Redirect to the welcome page.
        return redirect(url_for('home.welcome'))
    else:
        flash("Invalid password account has not been deactivated.",'error')