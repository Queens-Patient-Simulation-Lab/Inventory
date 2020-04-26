# Installation
Install python3, git, node, npm and pipenv from your preferred sources
1. `git clone https://github.com/Queens-Patient-Simulation-Lab/Inventory.git`
2. `cd Simulation-Lab`
3. `pipenv install` to install the backend dependencies
4. `npm install` to install the frontend dependencies

# Running
Run `npm run dev` to build the frontend.
You can use `npm run watch` to continuous build when the frontend files change.

You can start the server by running `pipenv shell` to spawn a shell inside the project and then running `python manage.py runsever`.

This can be combined into `pipenv run python manage.py runserver`

Alternatively, your IDE may have support for activating and debugging inside virtual enviroments. (VSCode Python extension does)

# Links
Great video series on using Django: https://www.youtube.com/watch?v=UmljXZIypDc


#Migrations
When any database models change, the person who changed it should generate a migration file with:
python manage.py makemigrations

To use the latest migration file, simply call:
python manage.py migrate

# Pre-populate data

(In development only): We created a command populate_db that pre-populates the database
To run it, call 'python manage.py populate_db'
To modify the command, view the class called populate_db.py
WARNING: This command will clear your development database (it will ask for confirmation)

# Tests
There are two types of tests: ModelTests and ViewTests
ModelTests checks the logic and functions of the models (e.g LocationModel)
ViewTests checks the Logic of views (e.g functions in views.py). These tests are validated by looking at the context returned from the response as well as seeing how the call affected the database. Note that you must simulate logging in to test secured views

# Font Awesome
Additional font aweseome glyphs can be imported from assets/js/font_awesome.js 