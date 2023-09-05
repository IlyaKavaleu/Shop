<h1>Store Server</h1>
The project for study Django.

<h3>Stack:</h3>
Python
PostgreSQL
Redis
Local Developing
All actions should be executed from the source directory of the project and only after installing all requirements.

<h3>Firstly, create and activate a new virtual environment:</h3>

python3.9 -m venv ../venv
source ../venv/bin/activate
Install packages:

pip install --upgrade pip
pip install -r requirements.txt
<Run project dependencies, migrations, fill the database with the fixture data etc.:

./manage.py migrate<
./manage.py loaddata <path_to_fixture_files>
./manage.py runserver
<h3>Run Redis Server:</h3>

redis-server
<h3>Run Celery:</h3>

celery -A store worker --loglevel=INFO
