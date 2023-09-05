<h1>Store Server</h1>
The project for study Django.

Stack:
<h3>Python</h3>
<h3>PostgreSQL</h3>
<h3>Redis</h3>
Local Developing
All actions should be executed from the source directory of the project and only after installing all requirements.

Firstly, create and activate a new virtual environment:

<h3>python3.9 -m venv ../venv</h3>
<h3>source ../venv/bin/activate</h3>
Install packages:

<h3>pip install --upgrade pip</h3>
<h3>pip install -r requirements.txt</h3>
<Run project dependencies, migrations, fill the database with the fixture data etc.:

<h3>./manage.py migrate</h3>
<h3>./manage.py loaddata <path_to_fixture_files></h3>
<h3>./manage.py runserver<h3>
Run Redis Server:

redis-server
Run Celery:

<h3>celery -A store worker --loglevel=INFO</h3>
