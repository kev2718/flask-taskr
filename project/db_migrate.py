from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()

    # temporarily change the name of tasks table
    c.execute("alter table users rename to old_users;")

    # recreate a new tasks table with updated schema
    db.create_all()

    # retrieve data from old_tasks table
    c.execute("select name, email, password from old_users order by id asc;")

    # save all rows as a list of tuples
    # set posted_date to now and user_id to 1
    data = [(row[0], row[1], row[2], 'user') for row in c.fetchall()]

    # insert data to tasks table
    c.executemany("insert into users (name, email, password) values (?, ?, ?);", data)

    # delete old_tasks table
    c.execute("drop table old_users;")
