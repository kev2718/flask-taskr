from project import db
import datetime

# this class defines the task-table
# this is how the create_all method knows to create our Task schema (extend)
class Task(db.Model):

    # variablenames stand for columns
    __tablename__ = "tasks"
    # primary_keys are auto set to auto-increment
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    posted_date = db.Column(db.Date, default=datetime.datetime.utcnow())
    status = db.Column(db.Integer)
    # define a foreignkey to another database
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # for each query set the values
    def __init__(self, name, due_date, priority, posted_date, status, user_id):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.posted_date = posted_date
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return "<name {0}>".format(self.name)

# this class represents the user table in the db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='user')
    # meta info that there is a relationship within this table to others
    # use task.poster (as a backref) as a query object in templates
    tasks = db.relationship("Task", backref="poster")

    def __init__(self, name=None, email=None, password=None, role=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return "<User {0}>".format(self.name)
