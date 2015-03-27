# weight/views.py
# Jake Malley
# 03/02/15

"""
Define all the routes for the weight blueprint.
"""

# Imports
from flask import flash, redirect, render_template, \
                request, url_for, Blueprint
from flask.ext.login import login_required, current_user
from traininglog.models import Weight
from traininglog import db
from forms import AddWeightForm
from datetime import datetime
from functools import wraps

# Setup the weight blueprint.
weight_blueprint = Blueprint(
    'weight', __name__,
    template_folder='templates'
    )

# Weight required, a decorator used to make sure users have 
# added a weight to the database. 
def weight_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Due to some errors with old users not having weight data, make sure the user has added weight data.
        if not current_user.weight_data:
            # If no data was found, redirect them to the add page.
            return redirect(url_for('weight.add_weight',error="You must add a weight to the database before continuing. Otherwise some applications may not work correctly."))
        return f(*args, **kwargs)
    return decorated_function

# Define the routes.
@weight_blueprint.route('/')
@login_required
def index():
    """
    Gets the the weight data and displays it to the user.
    """

    # Create a base query
    weight_data_query = Weight.query.filter_by(member=current_user).order_by(Weight.id.desc())
    # Get all the weight data.
    all_weight_data = weight_data_query.all()
    # Get the last 5 data points for a graph.
    limit_weight_data = weight_data_query.limit(5).all()

    # Get the chart data for the last t events.
    # Reverse the array so the newest is on the right.
    chart_data = [data.get_weight() for data in limit_weight_data][::-1]
    label_data = [data.get_date_str() for data in limit_weight_data][::-1]

    # Display the weight homepage.
    return render_template('weight_view_weight.html', add_weight_form=AddWeightForm(), weight_data=all_weight_data,chart_data=chart_data,label_data=label_data)

@weight_blueprint.route('/add',methods=['GET','POST'])
@login_required
def add_weight():
    """
    Displays a form to the user to allow them to add new 
    weight into the database.
    """

    # Create the form
    add_weight_form = AddWeightForm()

    # Create a error variable from the get arguments, otherwise default to none.
    error = request.args.get('error')

    # If the method was post.
    if request.method == 'POST':
        # Validate the form.
        if add_weight_form.validate_on_submit():
            # Form is valid add new database.

            # Get the time
            now = datetime.utcnow()

            last_weights = Weight.query.filter_by(member=current_user).filter(Weight.date >= now.date()).all()

            if len(last_weights) > 5:
                error = "You cannot change your weight more than 5 times per day, please try again tomorrow."
            else:

                # Add a new entry.
                db.session.add(Weight(add_weight_form.weight.data, now, current_user.get_id()))

                # Commit the changes.
                db.session.commit()

                # Flash a message to the user.
                flash("New weight successfully added.")

                # If it was successful redirect them to the index page.
                return redirect(request.referrer or url_for('weight.index'))

    # Display the add weight page.
    return render_template('weight_add_weight.html', add_weight_form=add_weight_form,error=error)