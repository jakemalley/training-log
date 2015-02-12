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
from traininglog.models import Member, Exercise, Weight, Message, RunningLookUp, CyclingLookUp, SwimmingLookUp
from traininglog import db
from datetime import datetime, date, timedelta
from querying_functions import *

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
                
                # Get users most recent weight.
                user_weight = Weight.query.filter_by(member=current_user).order_by(Weight.id.desc()).first().get_weight()

                calories_burned = (float(RunningLookUp.query.filter_by(id=add_running_form.exercise_level.data).first().calories_burned)/80)*user_weight*float(add_running_form.duration.data)

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
                
                # Get users most recent weight.
                user_weight = Weight.query.filter_by(member=current_user).order_by(Weight.id.desc()).first().get_weight()

                calories_burned = (float(CyclingLookUp.query.filter_by(id=add_cycling_form.exercise_level.data).first().calories_burned)/80)*user_weight*float(add_cycling_form.duration.data)
                
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
                
                # Get users most recent weight.
                user_weight = Weight.query.filter_by(member=current_user).order_by(Weight.id.desc()).first().get_weight()

                calories_burned = (float(SwimmingLookUp.query.filter_by(id=add_swimming_form.exercise_level.data).first().calories_burned)/80)*user_weight*float(add_swimming_form.duration.data)
            
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
    all_exercise_data = Exercise.query.filter_by(member=current_user).order_by(Exercise.id.desc()).all()

    return render_template('view.html',all_exercise_data=all_exercise_data,member=current_user)

@exercise_blueprint.route('/view/<exercise_id>')
@login_required
def view_exercise(exercise_id):
    """
    Page to display a single exercise event.
    Displays the event with the id = exercise_id
    """
    
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    if exercise.member != current_user:
        # If you are viewing another users exercise.
        db.session.add(Message(datetime.utcnow(), current_user.get_full_name()+" Viewed your exercise", exercise.member.get_id()))
        # Commit the changes.
        db.session.commit()

    all_exercise_data = Exercise.query.filter_by(member=exercise.member).order_by(Exercise.id.desc()).all()

    return render_template('view.html',all_exercise_data=all_exercise_data,exercise=exercise,member=exercise.member)

@exercise_blueprint.route('/compare/<member_id>')
@login_required
def compare(member_id):
    """
    Page to compare to users.
    """

    compare_member1 = current_user
    compare_member2 = Member.query.filter_by(id=member_id).first()

    # Get todays date.
    now = datetime.utcnow()

    compare_member1_data = {
                            "name":compare_member1.get_full_name(),
                            "total_time":get_exercise_total(datetime(now.year,1,1),member=compare_member1),
                            "total_cals":get_cals_total(datetime(now.year,1,1),member=compare_member1),
                            "running_time":get_hours_running(member=compare_member1),
                            "running_cals":get_cals_running(member=compare_member1),
                            "cycling_time":get_hours_cycling(member=compare_member1),
                            "cycling_cals":get_cals_cycling(member=compare_member1),
                            "swimming_time":get_hours_swimming(member=compare_member1),
                            "swimming_cals":get_cals_swimming(member=compare_member1),
                            }
    compare_member2_data = {
                            "name":compare_member2.get_full_name(),
                            "total_time":get_exercise_total(datetime(now.year,1,1),member=compare_member2),
                            "total_cals":get_cals_total(datetime(now.year,1,1),member=compare_member2),
                            "running_time":get_hours_running(member=compare_member2),
                            "running_cals":get_cals_running(member=compare_member2),
                            "cycling_time":get_hours_cycling(member=compare_member2),
                            "cycling_cals":get_cals_cycling(member=compare_member2),
                            "swimming_time":get_hours_swimming(member=compare_member2),
                            "swimming_cals":get_cals_swimming(member=compare_member2),
                            }

    return render_template('compare.html',compare_member1_data=compare_member1_data,compare_member2_data=compare_member2_data)

@exercise_blueprint.route('/picktheteam')
@login_required
def compare():
    """
    Page to display the team of eight runners.
    """

    return "Pick the team"

