release: python manage.py migrate && python manage.py create_admin; (python manage.py start_background_tasks &)
web: gunicorn simulation_lab.wsgi --log-file -