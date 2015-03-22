# exercise/views.py
# Jake Malley
# 01/02/15

"""
Define all of the routes for the exercise blueprint.
"""

# Imports 
from flask import flash, redirect, render_template, \
                request, url_for, Blueprint, abort
from flask.ext.login import login_required, current_user
from forms import AddRunningForm, AddCyclingForm, AddSwimmingForm, CompareMemberForm, EditExerciseForm
from traininglog.models import Member, Exercise, Weight, Message, RunningLookUp, CyclingLookUp, SwimmingLookUp
from traininglog import db
from datetime import datetime, date, timedelta
from querying_functions import *
from operator import itemgetter

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

    # Get all the current members.
    members = Member.query.all()
    # Create the choices list for the compare form.
    choices = [(member.get_id(), member.get_full_name()) for member in members]

    # Create the form.
    compare_form = CompareMemberForm()
    compare_form.compare_member_1.choices = choices
    compare_form.compare_member_2.choices = choices

    # Display the exercise home page passing in the forms and recent data etc.
    return render_template('index.html', add_running_form=add_running_form, add_swimming_form=add_swimming_form, add_cycling_form=add_cycling_form, exercise_data=exercise_data,compare_form=compare_form)

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

    # Display the add running page.
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

    # Display the add cycling page.
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

    # Display the add swimming page.
    return render_template('add_swimming.html', add_swimming_form=add_swimming_form, message=message, swimming_data=swimming_data)

@exercise_blueprint.route('/view')
@login_required
def view():
    """
    Page to display a table of all the users exercise.
    It allows users to then click on specific events,
    which can then be viewed with view_exercise
    """
    # Select the exercise data for the current member.
    all_exercise_data = Exercise.query.filter_by(member=current_user).order_by(Exercise.id.desc()).all()

    # Display the view page passing in all the exercise data.
    return render_template('view.html',all_exercise_data=all_exercise_data,member=current_user)

@exercise_blueprint.route('/view/<exercise_id>')
@login_required
def view_exercise(exercise_id):
    """
    Page to display a single exercise event.
    Displays the event with the id = exercise_id
    """
    
    # Get the exercise object with the given id.
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    if exercise is not None:

        # Create the edit exercise form.
        edit_exercise_form = EditExerciseForm()

        if exercise.member != current_user:
            # If you are viewing another users exercise.
            db.session.add(Message(datetime.utcnow(), current_user.get_full_name()+" Viewed your exercise", exercise.member.get_id()))
            # Commit the changes.
            db.session.commit()

        # Get all of the exercise for the member of the given exercise.
        all_exercise_data = Exercise.query.filter_by(member=exercise.member).order_by(Exercise.id.desc()).all()

    else:
        # The exercise ID is invalid abort with HTTP 404
        abort(404)

    # Display the view page for a specific exercise event.
    return render_template('view.html',all_exercise_data=all_exercise_data,exercise=exercise,member=exercise.member,edit_exercise_form=edit_exercise_form)

@exercise_blueprint.route('/edit_exercise', methods=['POST','GET'])
@login_required
def edit_exercise():
    """
    Allows users to edit their exercise.
    """

    # Create the edit exercise form.
    edit_exercise_form = EditExerciseForm()

    if request.method=='POST' and edit_exercise_form.validate_on_submit():
        # The method was post and the form was valid.
        # Get the exercise object.
        exercise = Exercise.query.filter_by(id=edit_exercise_form.exercise_id.data).first()
        # Check the exercise is for the current user.
        if exercise.member == current_user:
            # OK lets run the update.
            # See if the want us to delete it.
            if bool(edit_exercise_form.delete.data) == True:
                # Delete that exercise.
                db.session.delete(exercise)
                db.session.commit()
                flash("Exercise has been deleted.")
                # Send back to all the exercise as this event won't exist anymore.
                return redirect(url_for('exercise.view'))
            else:
                # Calculate the new calories burned.
                # (We don't want to include the new weight in case they did this when the weight was different etc.
                # we are only updating the duration and thus calories burned as only a result of this.)
                new_calories_burned = (exercise.calories_burned/exercise.exercise_duration)*float(edit_exercise_form.duration.data) 
                # Update the duration.
                exercise.update_duration(float(edit_exercise_form.duration.data), new_calories_burned)
                flash("Exercise has been updated.")
                
    # Send them back to where they came from.
    return redirect(request.referrer or url_for('exercise.index'))


@exercise_blueprint.route('/compare',methods=['POST','GET'])
@login_required
def compare():
    """
    Page to compare to users.
    """

    compare_form = CompareMemberForm()

    # Get all the current members.
    members = Member.query.all()
    # Create the choices list for the compare form.
    choices = [(member.get_id(), member.get_full_name()+' (id='+str(member.get_id())+')') for member in members]
    # Create the form.
    compare_form = CompareMemberForm()
    compare_form.compare_member_1.choices = choices
    compare_form.compare_member_2.choices = choices

    # Make sure the method was post.
    if request.method == 'POST':
        # Validate the form.
        if compare_form.validate_on_submit():
            # Get data from the compare form.

            # Get the member objects for both of the members select on the form.
            compare_member_1 = Member.query.filter_by(id=compare_form.compare_member_1.data).first()
            compare_member_2 = Member.query.filter_by(id=compare_form.compare_member_2.data).first()

            # Get todays date.
            now = datetime.utcnow()

            # Create compare data for member 1.
            compare_member_1_data = {
                                    "name":compare_member_1.get_full_name(),
                                    "total_time":get_exercise_total(datetime(now.year,1,1),member=compare_member_1),
                                    "total_cals":get_cals_total(datetime(now.year,1,1),member=compare_member_1),
                                    "running_time":get_hours_running(member=compare_member_1),
                                    "running_cals":get_cals_running(member=compare_member_1),
                                    "cycling_time":get_hours_cycling(member=compare_member_1),
                                    "cycling_cals":get_cals_cycling(member=compare_member_1),
                                    "swimming_time":get_hours_swimming(member=compare_member_1),
                                    "swimming_cals":get_cals_swimming(member=compare_member_1),
                                    }
            # Create compare data for member 2.
            compare_member_2_data = {
                                    "name":compare_member_2.get_full_name(),
                                    "total_time":get_exercise_total(datetime(now.year,1,1),member=compare_member_2),
                                    "total_cals":get_cals_total(datetime(now.year,1,1),member=compare_member_2),
                                    "running_time":get_hours_running(member=compare_member_2),
                                    "running_cals":get_cals_running(member=compare_member_2),
                                    "cycling_time":get_hours_cycling(member=compare_member_2),
                                    "cycling_cals":get_cals_cycling(member=compare_member_2),
                                    "swimming_time":get_hours_swimming(member=compare_member_2),
                                    "swimming_cals":get_cals_swimming(member=compare_member_2),
                                    }

            # Get most recent exercise for the charts
            compare_member_1_exercise = Exercise.query.filter_by(member=compare_member_1).order_by(Exercise.id.desc()).limit(5).all()
            compare_member_2_exercise = Exercise.query.filter_by(member=compare_member_2).order_by(Exercise.id.desc()).limit(5).all()

            # Chart data for time
            chart_data_time_1 = [ exercise.exercise_duration for exercise in compare_member_1_exercise][::-1]
            chart_data_time_2 = [ exercise.exercise_duration for exercise in compare_member_2_exercise][::-1]
            # Chart data for calories
            chart_data_calories_1 = [ exercise.calories_burned for exercise in compare_member_1_exercise][::-1]
            chart_data_calories_2 = [ exercise.calories_burned for exercise in compare_member_2_exercise][::-1]

            return render_template('compare.html',compare_member_1_data=compare_member_1_data,compare_member_2_data=compare_member_2_data, compare_form=compare_form,chart_data_time_1=chart_data_time_1,chart_data_time_2=chart_data_time_2,chart_data_calories_1=chart_data_calories_1,chart_data_calories_2=chart_data_calories_2)
    
    # Display the compare page.   
    return render_template('compare.html', compare_form=compare_form)

@exercise_blueprint.route('/picktheteam')
@login_required
def picktheteam():
    """
    Page to display the team of eight runners.
    """

    # Get all of the members in the database.
    members = Member.query.all()

    # Create a datetime object for this year.
    date = datetime(datetime.utcnow().year,1,1)

    # Get url argument to see if we need to display all the member or just the top 8.
    if request.args.get('all') == "true":
        page_title="All Members"
        pick_team=False
    else:
        page_title="Pick the Team"
        pick_team=True

    # Get url argument to see if we are ordering by calories_burned or total hours exercised.
    if request.args.get('order_by') == "hours":
        order_by = 2
    else: 
        order_by = 1

    # Create a new list for the ordered members to be stored in.
    members_ordered=[]

    # For each member.
    for member in members:

        # Calculate the total calories burned for that member this year.
        calories_burned = get_cals_total(date=date,member=member)
        # Calculate the total hours exercised for that member this year.
        hours_exercised = get_exercise_total(date=date, member=member)
        # Add a tuple of the member and the calories burned to the ordered members list.
        members_ordered.append((member, calories_burned, hours_exercised))

    # Actually order the list by the second element in each one. (The calories burned.)
    # (Reversing the list as it orders it in ascending order.)
    members_ordered = sorted(members_ordered, key=itemgetter(order_by))[::-1]
    
    # Display the page to pick the team.
    return render_template("exercise_picktheteam.html", page_title=page_title,pick_team=pick_team, members_ordered=members_ordered)