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


# Repository Structure

- migrations                 (Database migrations.)
   - versions                (Stores migration versions.)
- traininglog                (Training log package.)
   - dashboard               (Dashboard blueprint.)
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
