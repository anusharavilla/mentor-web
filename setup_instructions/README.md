# SETUP DEV AND HEROKU DEPLOYMENT

## DEVELOPMENT SET UP INSTRUCTIONS

### PYTHON UPDATE
pip install --upgrade pip

### VIRTUAL ENV
python3 -m venv <env_name>
source env_name/bin/activate

### REQUIREMENTS
pip install -r requirements.txt

### DATABASE 
Change the DATABASE_URL in setup.sh to reflect local database url and run:
source setup.sh

### MIGRATIONS FOR DATABASE SCHEMA UPDATE
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

### RUNNING THE SERVER
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload

## TEST SETUP
Edit TEST_DB_PATH and TEST_DB_NAME in test_script.sh and run it to test locally.
source test_script.sh

 

	
