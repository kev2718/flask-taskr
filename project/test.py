import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # each test should start with "test"
    def test_users_can_register(self):
        new_user = User("michael", "test@test.de", "michaelherman")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "michael"

    # login()
    # test if the call returns a 200 and the form has similar text
    def test_form_is_present(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list', response.data)

    # helper method for login a User
    def login(self, name, password):
        return self.app.post("/", data=dict(name=name, password=password), follow_redirects=True)

    # test if unregistered users can login
    def test_users_cannot_login_unless_registered(self):
        response = self.login("foo", "bar")
        self.assertIn(b'Invalid username or password', response.data)

    # helper method for register a users
    def register(self, name, email, password, confirm):
        return self.app.post("register/", data = dict(name=name, email=email, password=password, confirm=confirm), follow_redirects=True)

    # test if registered users can login (form validation is ok)
    def test_users_can_login(self):
        self.register("Michael", "michael@realpython.com", "python", "python")
        response = self.login("Michael", "python")
        self.assertIn(b'Welcome!', response.data)

    # test bad data to see how far the process gets
    def test_invalid_form_data(self):
        self.register("Michael", "michael@realpython.com", "python", "python")
        response = self.login("alert('alert box!');", "foo")
        self.assertIn(b'Invalid username or password', response.data)

    # test if form is present on register page
    def test_form_is_present_on_register_page(self):
        response = self.app.get("register/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list', response.data)

    # test if users can register (form validation is ok)
    def test_user_registration(self):
        self.app.get("register/", follow_redirects=True)
        response = self.register("Michael", "michael@realpython.com", "python", "python")
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    # test if there are registration errors (if same user registered)
    def test_user_registration_error(self):
        self.app.get("register/", follow_redirects=True)
        self.register("Michael", "michael@realpython.com", "python", "python")
        self.app.get("register/", follow_redirects=True)
        response = self.register("Michael", "michael@realpython.com", "python", "python")
        self.assertIn(b'That username and/or email already exist.', response.data)

    # helper method for logout a users
    def logout(self):
        return self.app.get("logout/", follow_redirects=True)

    # test if users can logout (only logged in users can logout)
    def test_logged_in_users_can_logout(self):
        self.register("Michael", "michael@realpython.com", "python", "python")
        self.login("Michael", "python")
        response = self.logout()
        self.assertIn(b'Goodbye', response.data)

    # test if not logged in users can logout
    def test_not_logged_in_users_can_logout(self):
        response = self.logout()
        self.assertIn(b'Goodbye', response.data)

    # test if users can access tasks
    def test_logged_in_users_can_access_tasks_page(self):
        self.register("Michael", "michael@realpython.com", "python", "python")
        self.login("Michael", "python")
        response = self.app.get("tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task', response.data)

    # test if not logged in unsers can acces task page
    def test_not_logged_in_users_can_access_tasks_page(self):
        response = self.app.get("tasks/", follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    # helper methods for creating tasks and users
    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post("add/", data=dict(
            name="Go to the bank",
            due_date="10/08/2016",
            priority="1",
            posted_date="10/08/2016",
            status="1"
        ), follow_redirects=True)

    # test if user can add tasks (form validation)
    def test_users_can_add_tasks(self):
        self.create_user("Michael", "michael@realpython.com", "python")
        self.login("Michael", "python")
        self.app.get("tasks/", follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'New entry was successfully posted. Thanks.', response.data)

    # test if theres an error in the above test
    def test_users_cannot_add_tasks_when_error(self):
        self.create_user("Michael", "michael@realpython.com", "python")
        self.login("Michael", "python")
        self.app.get("tasks/", follow_redirects=True)
        response = self.app.post("add/", data=dict(
            name="Go to the bank",
            due_date="",
            priority="1",
            posted_date="02/05/2014",
            status="1",
        ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    # test if user can complete a task
    def test_users_can_complete_tasks(self):
        self.create_user("Michael", "michael@realpython.com", "python")
        self.login("Michael", "python")
        self.app.get("tasks/", follow_redirects=True)
        self.create_task()
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertIn(b'The task was marked as complete. Nice.', response.data)

    # test if user can delete a task
    def test_users_can_delete_tasks(self):
        self.create_user("Michael", "michael@realpython.com", "python")
        self.login("Michael", "python")
        self.app.get("tasks/", follow_redirects=True)
        self.create_task()
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    # test if user A add a task and others can delete or mark as complete That
    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user("Michael", "michael@realpython.com", "python")
        self.login("Michael", "python")
        self.app.get("tasks/", follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user("Fletcher", "fletcher@realpython.com", "python101")
        self.login("Fletcher", "python101")
        self.app.get("tasks/", follow_redirects=True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'The task was marked as complete. Nice.', response.data)

if __name__ == "__main__":
    unittest.main()
