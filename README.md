Parkwood Vale Harriers Training Log
===================================

Training Log Application for the WJEC A Level Computing Extended Task.

The system allows users to sign-in and record their training. The top eight runners will get picked for the team to run in the charity event.

# Installation

After cloning the repository with: 
```bash
git clone https://github.com/jakemalley/training-log
```

Install virtualenv and create a new virtual environment. (Activating it too!)
```bash
pip install virtualenv 
virtualenv venv
source venv/bin/activate
```

Install the requirements. (Within the virtual environment.)
```bash
pip install -r requirements.txt
```

Run the application.
```bash
python manage.py runserver
```

Running in development mode.
```bash
export TRAINING_LOG_CONFIG='config.DevelopmentConfig'
python manage.py runserver
```

Running in production mode.
```bash
export TRAINING_LOG_CONFIG='config.ProductionConfig'
python manage.py runserver
```
Or alternatively use Tornado Server rather than Flask's development server.
```bash
python manage.py tornadoserver
```

# Repository Structure

- migrations                 (Database migrations.)
   - versions                (Stores migration versions.)
- traininglog                (Training log package.)
   - dashboard               (Dashboard blueprint.)
      - templates            (Blueprint templates.)
   - admin                   (Admin blueprint.)
      - templates            (Blueprint templates.)
   - exercise                (Exercise blueprint.)
      - templates            (Blueprint templates.)
   - home                    (Home blueprint.)
      - templates            (Blueprint templates.)
   - login                   (Login blueprint.)
      - templates            (Blueprint templates.)
   - static                  (Stores static content.)
      - css                  (CSS files.)
      - fonts                (Custom fonts.)
      - images               (Image files.)
      - js                   (JS files.)
   - templates               (Global templates.)
   - weight                  (Weight Blueprint.)
      - templates            (Blueprint templates.)

# Task Specification
Parkwood Vale Harriers is a running club. The club has many members who meet regularly to train and to race.

A group of members has decided to organise an event to raise money for local charities. They will choose a team of eight people who will run non-stop from John O’Groats to Land’s End, in the shortest time possible. They intend to organise the run as a relay with one person running each hour while others rest in the team’s minibus. Each runner will run three times per day and will have to be very fit.

The group of members has devised a suggested demanding training programme, which will include running, cycling and swimming. At the end of the training programme, a team of runners will be selected.

The runners want to be able to keep accurate records of their training.

The runners intend to use the system to monitor their progress as they train for the run. They want to be able to measure the improvement in their fitness and compare their performance with other members of the team.

The runners have provided you with information about the number of calories burned during one hour of exercise.

The running club has commissioned you to create a computer based system which will:
- allow the user to:
   - enter, store, retrieve and amend runners’ personal details
   - enter, store and retrieve runners’ training information
- allow runners to compare their performance with other runners in each of the three training activities.
- select the team.
