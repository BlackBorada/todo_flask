import pytest
from app import create_app, db
from app.models import User



def app():
    app = create_app('testing')
    app.config
