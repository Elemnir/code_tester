#!/bin/bash

# Establish the environment
source config.sh
source venv/bin/activate

# Install any migrations or requirements updates
pip install -r requirements.txt
./manage.py migrate

# Run the server
gunicorn -b 127.0.0.1:8011 -u gunicorn -g gunicorn tester.wsgi
