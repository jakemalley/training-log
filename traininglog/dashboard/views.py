# dashboard/views.py
# Jake Malley
# 23/01/15

"""
Define the routes for the dashboard blueprint.
"""

from flask import flash, redirect, render_template, \
                request, url_for, Blueprint
from flask.ext.login import login_required, current_user

# Setup the dashboard blueprint.
dashboard_blueprint = Blueprint(
    'dashboard',__name__,
    template_folder='templates'
    )

# Define the routes
@dashboard_blueprint.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')