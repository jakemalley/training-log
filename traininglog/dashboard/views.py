# dashboard/views.py
# Jake Malley
# 23/01/15

"""
Define the routes for the dashboard blueprint.
"""

from flask import flash, redirect, render_template, \
                request, url_for, Blueprint
from flask.ext.login import login_required, current_user
from traininglog.models import Exercise

# Setup the dashboard blueprint.
dashboard_blueprint = Blueprint(
    'dashboard',__name__,
    template_folder='templates'
    )

# Define the routes
@dashboard_blueprint.route('/')
@login_required
def dashboard():

    # Get all the exercise data.
    exercise_data = Exercise.query.filter_by(member=current_user).order_by(Exercise.id.desc()).limit(8).all()

    chart_data = [{
                    'value': 25,
                    'color':"#F7464A",
                    'highlight': "#FF5A5E",
                    'label': "Running"
                },
                {
                    'value': 25,
                    'color': "#46BFBD",
                    'highlight': "#5AD3D1",
                    'label': "Swimming"
                },
                {
                    'value': 50,
                    'color': "#FDB45C",
                    'highlight': "#FFC870",
                    'label': "Cycling"
                }]

    return render_template('dashboard.html',chart_data=chart_data, exercise_data=exercise_data)