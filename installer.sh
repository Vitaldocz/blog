#!/usr/bin/env bash

dpkg -s 'virtualenv' &> /dev/null

if [[ $? -eq 0 ]]; then
    pass
else
    python3 -m pip install --user virtualenv
fi

python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

cd src/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
