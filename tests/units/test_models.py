from datetime import datetime
from app.models import Users, Task


def test_new_user():
    user = Users(username="test", email="test@test.com", password="test")
    assert user.username == "test"
    assert user.email == "test@test.com"
    assert user.password_hash != "test"
    assert user.__repr__() == "<User: test>"


def test_new_user_with_fixtures(new_user):
    assert new_user.username == "test_user"
    assert new_user.email == "test_user@example.com"
    assert new_user.password_hash != "password"
    assert new_user.__repr__() == "<User: test_user>"


def test_setting_password(new_user):
    new_user.set_password("NewPassword")
    assert new_user.password_hash != "NewPassword"
    assert new_user.check_password("NewPassword")
    assert not new_user.check_password("wrong_password")
    assert not new_user.check_password("NewPassword1")


def test_user_id(new_user):
    new_user.id = 10
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == "10"


def test_new_task():
    task = Task(
        title="test",
        description="test",
        due_date=datetime(2024, 6, 5, 0, 0, 0),
        completed=False,
        user_id=1,
    )
    assert task.title == "test"
    assert task.description == "test"
    assert task.due_date == datetime(2024, 6, 5, 0, 0, 0)
    assert task.completed is False
    assert task.user_id == 1
    assert (
        task.__repr__()
        == "Task('test', \
        'test', \
        '2024-06-05 00:00:00', \
        'False')"
    )
