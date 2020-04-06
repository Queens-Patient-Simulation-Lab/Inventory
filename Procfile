release: python manage.py migrate && python manage.py create_admin
web: gunicorn simulation_lab.wsgi --log-file -