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
Edit TEST_DB_PATH and TEST_DB_NAME in test_script.sh and run it to test locally:   
source test_script.sh

## DEPLOY TO HEROKU 
1. Create an account in heroku:   
    www.heroku.com  
2. Install Heroku by running:   
    brew tap heroku/brew && brew install heroku  
3. Use this command and login to heroku from terminal  
    heroku login  
4. Create heroku app  
    heroku create name_of_your_app  
5. Add git remote for heroku to local repository  
    git remote add heroku heroku_git_url  
6. Postgres add on for database  
    heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application  
7. To check config variables:  
    heroku config --app name_of_your_application  
    Add your config variables in the REVEAL CONFIG VARS section of setting on the heroku website  
8. To deploy run:  
    git push heroku master  
9. Run migrations using:  
    heroku run python manage.py db upgrade --app name_of_your_application 

	
