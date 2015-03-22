# admin/views.py
# Jake Malley
# 19/02/15

"""
Define the routes for the admin blueprint.
"""

# Imports
from flask import redirect, render_template, \
                request, url_for, Blueprint, abort, flash
from flask.ext.login import fresh_login_required, current_user
from traininglog import db
from traininglog.models import Member, Exercise
from forms import AdminEditDetailsForm
from functools import wraps
from datetime import datetime

# Setup the admin blueprint.
admin_blueprint = Blueprint(
    'admin',__name__,
    template_folder='templates'
    )

# Admin Required - Only allows members with is_admin = 1 to access these views.
# Allows me to use the decorator @admin_required on different routes.
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If they are not an admin take them home.
        if not bool(current_user.is_admin):
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    return decorated_function

# Define the routes
@admin_blueprint.route('/')
@fresh_login_required
@admin_required
def dashboard():
    """
    The dashboard for the admin blueprint.
    """

    # Get a list of all the members.
    members = Member.query.all()
    # Get a list of all the active members. (Members who have logged in today.)
    active_members = Member.query.filter(Member.last_login_date>datetime.utcnow().date()).all()
    # Create a dictionary of the stats.
    stats = {
                "total_members":len(members), # Total number of members.
                "active_members":len(active_members) # Total number of active members.
            }

    # Render the admin index page passing in the members and stats.
    return render_template('admin_index.html', members=members,stats=stats)

@admin_blueprint.route('/view/<member_id>', methods=['POST','GET'])
@fresh_login_required
@admin_required
def view(member_id):
    """
    Method for viewing individual users.
    """

    # Create the form to edit the members data.
    admin_edit_form = AdminEditDetailsForm()
    # If the method was post and the form was valid.
    if request.method == 'POST' and admin_edit_form.validate_on_submit():
        # Change the data.

        # Get the member with that ID.
        member = Member.query.filter_by(id=admin_edit_form.member_id.data).first()

        # See if the account was marked to be delete as then we don't need to update the details as well.
        if bool(admin_edit_form.delete_user.data) == True:
            # Delete the user.
            
            # Get their exercise data. 
            exercise_data = Exercise.query.filter_by(member=member).all()
            # For each piece of data.
            for data in exercise_data:
                # Delete the data.
                db.session.delete(data)

            # Finally delete the user.
            db.session.delete(member)
            # And commit the changes
            db.session.commit()

            # Flash a message.
            flash('Account has been delete!')

            # Redirect to the admin dashboard sicne that user doesn't exist anymore.
            return redirect(url_for('admin.dashboard'))

        else:
            # User was not marked as deleted, 
            # update their details with the details from the form.
            member.firstname = admin_edit_form.firstname.data
            member.surname = admin_edit_form.surname.data
            member.email = admin_edit_form.email.data
            member.set_active_status(int(admin_edit_form.set_active.data))
            member.is_admin = int(admin_edit_form.set_admin.data)

            # If the password was changed.
            if admin_edit_form.password.data:
                # Update the password.
                member.update_password(admin_edit_form.password.data)

            # Flash a success message.
            flash("Details have been updated. Please inform the member of the changes.")

        # Commit the changes.
        db.session.commit()

        # Refresh the page
        return render_template('admin_view.html', member=member, admin_edit_form=admin_edit_form)

    else:

        # Get the member with that ID.
        member = Member.query.filter_by(id=member_id).first()

        # If that member exists.
        if member is not None:
			# Render the template passing in the member and form.
            return render_template('admin_view.html', member=member, admin_edit_form=admin_edit_form)
        else:
			# Raise a HTTP 404 (Page not found) error.
            abort(404)