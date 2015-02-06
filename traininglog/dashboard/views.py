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
from datetime import datetime

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

    # Data for the pie chart
    pie_chart_data = [{
                    'value': get_hours_running(),
                    'color':"#F7464A",
                    'highlight': "#FF5A5E",
                    'label': "Hours Running"
                },
                {
                    'value': get_hours_swimming(),
                    'color': "#46BFBD",
                    'highlight': "#5AD3D1",
                    'label': "Hours Swimming"
                },
                {
                    'value': get_hours_cycling(),
                    'color': "#FDB45C",
                    'highlight': "#FFC870",
                    'label': "Hours Cycling"
                }]

    # Data for the line chart.
    line_chart_data = [data.get_calories_burned() for data in exercise_data][::-1]
    # Empty labels for the line chart.
    line_chart_labels = [data.get_datetime() for data in exercise_data][::-1]

    # Get todays date.
    now = datetime.utcnow()

    # Get total exercised for this year.
    exercise_total_year = get_exercise_total(datetime(now.year,1,1))
    exercise_total_today = get_exercise_total(now)

    progress_today_width = int(float(exercise_total_today/4)*100)
    progress_year_width = int(float(exercise_total_today/1460)*100)

    return render_template('dashboard.html',pie_chart_data=pie_chart_data, exercise_data=exercise_data,line_chart_data=line_chart_data,line_chart_labels=line_chart_labels,exercise_total_year=exercise_total_year,exercise_total_today=exercise_total_today,progress_today_width=progress_today_width,progress_year_width=progress_year_width)

def get_hours_running():
    """ 
    Returns the total hours of running.
    """
    exercise_data = Exercise.query.filter_by(member=current_user,exercise_type='running').all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total

def get_hours_cycling():  
    """ 
    Returns the total hours of cycling.
    """ 
    exercise_data = Exercise.query.filter_by(member=current_user,exercise_type='cycling').all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total

def get_hours_swimming(): 
    """ 
    Returns the total hours of swimming.
    """
    exercise_data = Exercise.query.filter_by(member=current_user,exercise_type='swimming').all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total

def get_exercise_total(date):
    """
    Returns the number of hours exercised on the date given.
    """
    exercise_data = Exercise.query.filter(Exercise.date>date.date()).filter_by(member=current_user).all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total