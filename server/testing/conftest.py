#!/usr/bin/env python3

import pytest
from app import app, db
from models import User

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))


@pytest.fixture(autouse=True)
def setup_database():
    with app.app_context():
        db.create_all()
        
        User.query.delete()
        
        users = [
            User(id=1, username="testuser1"),
            User(id=2, username="testuser2"),
        ]
        
        db.session.add_all(users)
        db.session.commit()
        
        yield
        
        db.session.remove()
        db.drop_all()