# dataPrivacy

dataPrivacy is our CMSC 447 Software Engineering group project.

The goal of dataPrivacy is to educate of people using social media sites, and improve their literacy in who is collecting their user data and what they are doing with it.

## Heroku Deployed Website:

The Heroku deployed can be found [here](dataprivacy.herokuapp.com) This and all future iterations will have completed work shown on this web link.

## How to run our app:

dataPrivacy is built using the Django we framework. To use this app you must download Django (you can follow [this](https://www.djangoproject.com/download/) documentation to make things easier

Once downloaded, clone dataPrivacy from this github repository and using a command line app cd into the root package directory (you should see manage.py among the list of available files in this directory)

to run - use the command

```
python manage.py runserver

```

## How to run our Tests:

Since we are only in the first iteration, unit testing does not test any logic. You can see our tests written in DataPrivacy/dataPrivacy/page/tests.py

To run our unit tests you can remain in the same directory (dataprivacy/)where manage.py is still available to use. and run the command:

```
python manage.py test

```

our tests will begin once run.


pip installs: pip install requests, pip install allauth, pip install django-allauth, pip install google-api-python-client, pip install google-auth-oauthlib
