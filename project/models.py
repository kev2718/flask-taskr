from views import db

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
    status = db.Column(db.Integer)

    def __init__(self, name, due_date, priority, status):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def __repr__(self):
        return "<name {0}>".format(self.name)
