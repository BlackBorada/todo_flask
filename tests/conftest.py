import pytest
from app import create_app, db
from app.models import User, Task

# --------
# Fixtures
# --------



@pytest.fixture(scope='module')
def new_user():
    user = User("test_user", email="test_user@example.com", password="password")
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    with flask_app.test_client() as testting_client:
        with flask_app.app_context():
            yield testting_client


@pytest.fixture(scope='module')
def init_database():

    db.create_all()

    first_user = User("first_user", email="first_user@example.com", password="password1")
    second_user = User("second_user", email="second_user@example.com", password="password2")

    db.session.add(first_user)
    db.session.add(second_user)

    db.session.commit()

    task1 = Task(title="task1", description="description1", completed=False, user_id=first_user.id)
    task2  = Task(title="task2", description="description2", completed=False, user_id=second_user.id)
    task3   = Task(title="task3", description="description3", completed=True, user_id=first_user.id)
    task4    = Task(title="task4", description="description4", completed=True, user_id=second_user.id)

    db.session.add(task1)
    db.session.add(task2)
    db.session.add(task3)
    db.session.add(task4)

    db.session.commit()

    db.drop_all()


    
