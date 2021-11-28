# Social-App

Social app built with django restframework.

The app consists of the following functionalities:

User sign-up
User login
Post creation
Post update
Post deletion
List Posts
Like post
unlike post

Steps to follow when running the application:

# Step 1
clone the project or download the zip and extract into a directory on your pc

# Step 2
set the following environment variables on host machine to api keys gotten from abstract api 
abstract_api_email_validation_api_key
abstract_api_ip_geolocation_api_key
abstract_api_holidays_api_key

# Step 3 Pip install the requirements
  - pip install -r requirements.txt
# Step 4 Run migrations
  - python manage.py makemigrations
  - python manage.py migrate
# Step 5 run the applicaion server
  - python manage.py runserver 0.0.0.0:8000
# Step 6 run celery from the terminal
  - celery -A social -l INFO"
# OR

Run with Docker
# Step 1
cd into the project directory and run the docker-compose comand below
  - docker-compose build .
# Step 2
  - docker-compose up -d
(the tests are set to run from the docker-compose file)

The application should be running on port 8000 on your host machine

# To run the tests manually from the terminal run:
  - python manage.py test social_app.tests
