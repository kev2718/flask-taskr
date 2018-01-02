# sets up and creates the database
from project import db

# create the database
db.create_all()

# commit changes
db.session.commit()
