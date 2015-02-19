# admin/views.py
# Jake Malley
# 19/02/15

"""
Define the routes for the admin blueprint.
"""

from flask import redirect, render_template, \
                request, url_for, Blueprint, abort, flash
from flask.ext.login import fresh_login_required, current_user
from traininglog import db
from traininglog.models import Member
from forms import AdminEditDetailsForm
from functools import wraps
from datetime import datetime

# Setup the admin blueprint.
admin_blueprint = Blueprint(
    'admin',__name__,
    template_folder='templates'
    )

# Admin Required - Only allows members with is_admin = 1 access these views.
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
    members = Member.query.all()
    active_members = Member.query.filter(Member.last_login_date>datetime.utcnow().date()).all()
    stats = {
                "total_members":len(members),
                "active_members":len(active_members)
            }

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
        member.firstname = admin_edit_form.firstname.data
        member.surname = admin_edit_form.surname.data
        member.email = admin_edit_form.email.data
        member.set_active_status(int(admin_edit_form.set_active.data))
        member.is_admin = int(admin_edit_form.set_admin.data)

        print("STOP")
        print(int(admin_edit_form.set_active.data))

        # If the password was changed.
        if admin_edit_form.password.data:
            # Update the password.
            member.update_password(admin_edit_form.password.data)

        # Commit the changes.
        db.session.commit()
        # Flash a success message.
        flash("Details have been updated. Please inform the member of the changes.")

        # Refresh the page
        return render_template('admin_view.html', member=member, admin_edit_form=admin_edit_form)

    else:

        # Get the member with that ID.
        member = Member.query.filter_by(id=member_id).first()

        # If that member exists.
        if member is not None:
            return render_template('admin_view.html', member=member, admin_edit_form=admin_edit_form)
        else:
            abort(404)



