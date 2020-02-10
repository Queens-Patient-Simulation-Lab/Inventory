release: python manage.py migrate && echo yes | python manage.py populate_db
web: gunicorn simulation_lab.wsgi --log-file -