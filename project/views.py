# contain the business logic(controller)
from forms import AddTaskForm, RegisterForm, LoginForm

from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import datetime

# config - defines db set to models.py and import Task table
app = Flask(__name__)
app.config.from_object("_config")
db = SQLAlchemy(app)

from models import Task, User

# helper functions

# decorates a function that a logged_in session variable is required to use it
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for("login"))
    return wrap

# route handlers
# all session variables must be popped when a user loggs out
@app.route("/logout/")
@login_required
def logout():
    session.pop("logged_in", None)
    session.pop("user_id", None)
    session.pop("role", None)
    flash("Goodbye!")
    return redirect(url_for("login"))

# login handler
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form["name"]).first()
            if user is not None and user.password == request.form["password"]:
                session["logged_in"] = True
                # save logged in user id so that tasks can be matched with names
                session["user_id"] = user.id
                session["role"] = user.role
                flash("Welcome!")
                return redirect(url_for("tasks"))
            else:
                error = "Invalid username or password."
    return render_template("login.html", form=form, error=error)

# get all tasks -> open and closed and display them in the task.html template
@app.route("/tasks/")
@login_required
def tasks():
    return render_template("tasks.html", form=AddTaskForm(request.form), open_tasks=open_tasks(), closed_tasks=closed_tasks())

# Add new tasks
@app.route("/add/", methods=["GET", "POST"])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            # grab the user id of logged in user who posted a new task
            new_task = Task(form.name.data, form.due_date.data, form.priority.data, datetime.datetime.utcnow(), "1", session["user_id"])
            db.session.add(new_task)
            db.session.commit()
            flash("New entry was successfully posted. Thanks.")
            return redirect(url_for("tasks"))
    return render_template("tasks.html", form=form, error=error, open_tasks=open_tasks(), closed_tasks=closed_tasks())

# Mark tasks as complete
@app.route("/complete/<int:task_id>/")
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session["role"] == "admin":
        task.update({"status": "0"})
        db.session.commit()
        flash("The task is complete. Nice.")
        return redirect(url_for("tasks"))
    else:
        flash("You can only update tasks that belong to you.")
        return redirect(url_for("tasks"))

# Delete tasks
@app.route("/delete/<int:task_id>/")
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session["role"] == "admin":
        task.delete()
        db.session.commit()
        flash("The task was deleted. Why not add a new one?")
        return redirect(url_for("tasks"))
    else:
        flash("You can only delete tasks that belong to you.")
        return redirect(url_for("tasks"))

# register form
@app.route("/register/", methods=["GET", "POST"])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(form.name.data, form.email.data, form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Thanks for registering. Please login.")
                return redirect(url_for("login"))
            except IntegrityError:
                error = "That username and/or email already exist."
                render_template("register.html", form=form, error=error)
    return render_template("register.html", form=form, error=error)

# flash all given errors
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field %s" % (getattr(form, field).label.text, error), "error")

# helper function for getting all open_tasks
def open_tasks():
    return db.session.query(Task).filter_by(status="1").order_by(Task.due_date.asc())

# helper function for getting all closed_tasks
def closed_tasks():
    return db.session.query(Task).filter_by(status="0").order_by(Task.due_date.asc())
