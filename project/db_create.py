# sets up and creates the database
import sqlite3

from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()
    c.execute("""create table tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    due_date TEXT NOT NULL,
                                    priority INTEGER NOT NULL,
                                    status INTEGER NOT NULL);""")
    c.execute("""insert into tasks(name, due_date, priority, status)
                    values('Finish this tutorial', '21/11/2017', 10, 1)""")
    c.execute("""insert into tasks(name, due_date, priority, status)
                    values('Finish Real Python Course 2', '21/11/2017', 10, 1);""")
