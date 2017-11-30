from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()

    # temporarily change the name of tasks table
    c.execute("alter table tasks rename to old_tasks;")

    # recreate a new tasks table with updated schema
    db.create_all()

    # retrieve data from old_tasks table
    c.execute("select name, due_date, priority, status from old_tasks order by task_id asc;")

    # save all rows as a list of tuples
    # set posted_date to now and user_id to 1
    data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in c.fetchall()]

    # insert data to tasks table
    c.executemany("insert into tasks (name, due_date, priority, status, posted_date, user_id) values (?, ?, ?, ?, ?, ?);", data)

    # delete old_tasks table
    c.execute("drop table old_tasks;")
