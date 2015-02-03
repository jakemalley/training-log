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
from datetime import datetime, date, timedelta

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

    # Get all the exercise data.
    exercise_data = Exercise.query.filter_by(member=current_user).order_by(Exercise.id.desc()).limit(10).all()

    return render_template('index.html', add_running_form=add_running_form, add_swimming_form=add_swimming_form, add_cycling_form=add_cycling_form, exercise_data=exercise_data)

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
            
            # Get the current time.
            now = datetime.utcnow()

            # Get the last post.
            last_post = Exercise.query.filter_by(member=current_user).order_by(Exercise.id.desc()).first()

            # Check to see if there was a last post.
            if last_post:
                # If there was set last_post_date to the date on the post.
                last_post_date = last_post.date
            else:
                # Create an empty datetime object with just todays date no time.
                last_post_date = datetime(now.year,now.month,now.day)

            # Make sure they aren't cheating by having more than 24 hours in one day.
            # And they haven't added a post in the last 30 seconds. i.e. they aren't rapidly clicking the button.
            if (get_exercise_total(now) + float(add_running_form.duration.data) <= 24) and ((last_post_date + timedelta(seconds=30)) < now):
                # Look Up the calories burned and commit it.
                # NEED TO DIVIDE THIS BY THE WEIGHT!
                calories_burned = (RunningLookUp.query.filter_by(id=add_running_form.exercise_level.data).first().calories_burned)*add_running_form.duration.data
                # Add the exercise to the database.
                db.session.add(Exercise(now, 'running', add_running_form.exercise_level.data, add_running_form.duration.data, calories_burned, current_user.get_id()))
                # Commit the changes.
                db.session.commit()
                # Flash a success message.
                flash("Exercise successfully added.")
                # Add a well done message.
                message = "Well Done you burned "+str(calories_burned)+" calories in that session."
            else:
                # Make the correct error message.
                flash("An error occurred adding that exercise.",'error')
                if (get_exercise_total(now) + float(add_running_form.duration.data) > 24):
                    message = "Exercise has not been added as the current total for today exceeds 24 hours."
                else:
                    message = "You have tried to add too many events in the last 30 seconds, please wait then try again."

    # Get the last 4 exercises for running.
    running_data = Exercise.query.filter_by(exercise_type='running',member=current_user).order_by(Exercise.id.desc()).limit(4).all()

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

            # Get the current time.
            now = datetime.utcnow()

            # Get the last post.
            last_post = Exercise.query.filter_by(member=current_user).order_by(Exercise.id.desc()).first()

            # Check to see if there was a last post.
            if last_post:
                # If there was set last_post_date to the date on the post.
                last_post_date = last_post.date
            else:
                # Create an empty datetime object with just todays date no time.
                last_post_date = datetime(now.year,now.month,now.day)

            # Make sure they aren't cheating by having more than 24 hours in one day.
            # And they haven't added a post in the last 30 seconds. i.e. they aren't rapidly clicking the button.
            if (get_exercise_total(now) + float(add_cycling_form.duration.data) <= 24) and ((last_post_date + timedelta(seconds=30)) < now):
                # Look Up the calories burned and commit it.
                # NEED TO DIVIDE THIS BY THE WEIGHT!
                calories_burned = (CyclingLookUp.query.filter_by(id=add_cycling_form.exercise_level.data).first().calories_burned)*add_cycling_form.duration.data
                
                # Add the exercise to the database.
                db.session.add(Exercise(now, 'cycling', add_cycling_form.exercise_level.data, add_cycling_form.duration.data, calories_burned, current_user.get_id()))
                # Commit the changes.
                db.session.commit()
                # Flash a success message.
                flash("Exercise successfully added.")
                # Add a well done message.
                message = "Well Done you burned "+str(calories_burned)+" calories in that session."
            else:
                # Make the correct error message.
                flash("An error occurred adding that exercise.",'error')
                if (get_exercise_total(now) + float(add_cycling_form.duration.data) > 24):
                    message = "Exercise has not been added as the current total for today exceeds 24 hours."
                else:
                    message = "You have tried to add too many events in the last 30 seconds, please wait then try again."

    # Get the last 4 exercises for running.
    cycling_data = Exercise.query.filter_by(exercise_type='cycling',member=current_user).order_by(Exercise.id.desc()).limit(4).all()

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

            # Get the current time.
            now = datetime.utcnow()

            # Get the last post.
            last_post = Exercise.query.filter_by(member=current_user).order_by(Exercise.id.desc()).first()

            # Check to see if there was a last post.
            if last_post:
                # If there was set last_post_date to the date on the post.
                last_post_date = last_post.date
            else:
                # Create an empty datetime object with just todays date no time.
                last_post_date = datetime(now.year,now.month,now.day)

            # Make sure they aren't cheating by having more than 24 hours in one day.
            # And they haven't added a post in the last 30 seconds. i.e. they aren't rapidly clicking the button.
            if (get_exercise_total(now) + float(add_swimming_form.duration.data) <= 24) and ((last_post_date + timedelta(seconds=30)) < now):
                # Look Up the calories burned and commit it.
                # NEED TO DIVIDE THIS BY THE WEIGHT!
                calories_burned = (SwimmingLookUp.query.filter_by(id=add_swimming_form.exercise_level.data).first().calories_burned)*add_swimming_form.duration.data
            
                # Add the exercise to the database.
                db.session.add(Exercise(now, 'swimming', add_swimming_form.exercise_level.data, add_swimming_form.duration.data, calories_burned, current_user.get_id()))
                # Commit the changes.
                db.session.commit()
                # Flash a success message.
                flash("Exercise successfully added.")
                # Add a well done message.
                message = "Well Done you burned "+str(calories_burned)+" calories in that session."
            else:
                # Make the correct error message.
                flash("An error occurred adding that exercise.",'error')
                if (get_exercise_total(now) + float(add_swimming_form.duration.data) > 24):
                    message = "Exercise has not been added as the current total for today exceeds 24 hours."
                else:
                    message = "You have tried to add too many events in the last 30 seconds, please wait then try again."

    # Get the last 4 exercises for running.
    swimming_data = Exercise.query.filter_by(exercise_type='swimming',member=current_user).order_by(Exercise.id.desc()).limit(4).all()

    return render_template('add_swimming.html', add_swimming_form=add_swimming_form, message=message, swimming_data=swimming_data)

@exercise_blueprint.route('/view')
@login_required
def view():
    """
    Page to display a table of all the users exercise.
    It allows users to then click on specific events,
    which can then be viewed with view_exercise
    """
    pass

@exercise_blueprint.route('/view/<exercise_id>')
@login_required
def view_exercise(exercise_id):
    """
    Page to display a single exercise event.
    Displays the event with the id = exercise_id
    """

    exercise = Exercise.query.filter_by(id=exercise_id).first()

# Querying Functions
def get_exercise_total(date):
    """
    Returns the number of hours exercised on the date given.
    """
    exercise_data = Exercise.query.filter(Exercise.date>date.date()).filter_by(member=current_user).all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total
