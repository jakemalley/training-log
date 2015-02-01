# exercise/views.py
# Jake Malley
# 01/02/15

"""
Define all of the routes for the exercise blueprint.
"""

from flask import flash, redirect, render_template, \
                request, url_for, Blueprint
from flask.ext.login import login_required, current_user
from forms import AddRunningForm, AddCyclingForm, AddSwimmingForm
from traininglog.models import Member, Exercise, RunningLookUp, CyclingLookUp, SwimmingLookUp
from traininglog import db
from datetime import datetime

# Setup the exercise blueprint.
exercise_blueprint = Blueprint(
    'exercise', __name__,
    template_folder='templates'
    )

# Define the routes
@exercise_blueprint.route('/')
@login_required
def index():
    """
    Homepage for all the exercise data.
    Displays forms for adding exercise, options for generating reports 
    then a table for all the exercise.
    """

    # Create all of the forms.
    add_running_form = AddRunningForm()
    add_cycling_form = AddCyclingForm()
    add_swimming_form = AddSwimmingForm()


    return render_template('index.html', add_running_form=add_running_form, add_swimming_form=add_swimming_form, add_cycling_form=add_cycling_form)

@exercise_blueprint.route('/add_running', methods=['GET','POST'])
@login_required
def add_running():
    """
    Displays a form for users to add running.
    """

    # Create the running form.
    add_running_form = AddRunningForm()

    # Create empty message.
    message = None

    # Make sure the method was post.
    if request.method == 'POST':
        # Validate the form.
        if add_running_form.validate_on_submit():
            # Look Up the calories burned and commit it.
            # NEED TO DIVIDE THIS BY THE WEIGHT!
            calories_burned = (RunningLookUp.query.filter_by(id=add_running_form.exercise_level.data).first().calories_burned)*add_running_form.duration.data
            # Get the current time.
            now = datetime.utcnow()
            # Add the exercise to the database.
            db.session.add(Exercise(now, 'running', add_running_form.exercise_level.data, add_running_form.duration.data, calories_burned, current_user.get_id()))
            # Commit the changes.
            db.session.commit()
            # Flash a success message.
            flash("Exercise successfully added.")
            # Add a well done message.
            message = "Well Done you burned "+str(calories_burned)+" calories in that session."

    # Get the last 4 exercises for running.
    running_data = Exercise.query.filter_by(exercise_type='running').order_by(Exercise.id.desc()).limit(4).all()

    return render_template('add_running.html', add_running_form=add_running_form, message=message,running_data=running_data)

@exercise_blueprint.route('/add_cycling', methods=['GET','POST'])
@login_required
def add_cycling():
    """
    Displays a form for users to add cycling.
    """

    # Create empty message.
    message = None

    # Create the cycling form.
    add_cycling_form = AddCyclingForm()

    # Make sure the method was post.
    if request.method == 'POST':
        # Validate the form.
        if add_cycling_form.validate_on_submit():
            # Look Up the calories burned and commit it.
            # NEED TO DIVIDE THIS BY THE WEIGHT!
            calories_burned = (CyclingLookUp.query.filter_by(id=add_cycling_form.exercise_level.data).first().calories_burned)*add_cycling_form.duration.data
            # Get the current time.
            now = datetime.utcnow()
            # Add the exercise to the database.
            db.session.add(Exercise(now, 'cycling', add_cycling_form.exercise_level.data, add_cycling_form.duration.data, calories_burned, current_user.get_id()))
            # Commit the changes.
            db.session.commit()
            # Flash a success message.
            flash("Exercise successfully added.")
            # Add a well done message.
            message = "Well Done you burned "+str(calories_burned)+" calories in that session."

    # Get the last 4 exercises for running.
    cycling_data = Exercise.query.filter_by(exercise_type='cycling').order_by(Exercise.id.desc()).limit(4).all()

    return render_template('add_cycling.html', add_cycling_form=add_cycling_form, message=message, cycling_data=cycling_data)
    
@exercise_blueprint.route('/add_swimming', methods=['GET','POST'])
@login_required
def add_swimming():
    """
    Displays a form for users to add swimming.
    """

    # Create empty message.
    message=None

    # Create the swimming form.
    add_swimming_form = AddSwimmingForm()

    # Make sure the method was post.
    if request.method == 'POST':
        # Validate the form.
        if add_swimming_form.validate_on_submit():
            # Look Up the calories burned and commit it.
            # NEED TO DIVIDE THIS BY THE WEIGHT!
            calories_burned = (SwimmingLookUp.query.filter_by(id=add_swimming_form.exercise_level.data).first().calories_burned)*add_swimming_form.duration.data
            # Get the current time.
            now = datetime.utcnow()
            # Add the exercise to the database.
            db.session.add(Exercise(now, 'swimming', add_swimming_form.exercise_level.data, add_swimming_form.duration.data, calories_burned, current_user.get_id()))
            # Commit the changes.
            db.session.commit()
            # Flash a success message.
            flash("Exercise successfully added.")
            # Add a well done message.
            message = "Well Done you burned "+str(calories_burned)+" calories in that session."

    # Get the last 4 exercises for running.
    swimming_data = Exercise.query.filter_by(exercise_type='swimming').order_by(Exercise.id.desc()).limit(4).all()

    return render_template('add_swimming.html', add_swimming_form=add_swimming_form, message=message, swimming_data=swimming_data)

