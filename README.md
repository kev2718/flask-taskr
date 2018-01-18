# flask-taskr
This is a simple Taskmanager written in Python with Microframework [Flask](http://flask.pocoo.org/ "Flask Homepage").

## Install and setting up
Install dependencies
`pip install -r requirements.txt`

Setting up Database
`python db_create.py`

Running local Server
`python run.py`

Launching Webapp
http://localhost:5000

## RESTful API
Call `localhost:5000/api/v1/tasks/` for a json Object of all Tasks

and `localhost:5000/api/v1/tasks/<int:task_id>` for a json Object of a single Task
