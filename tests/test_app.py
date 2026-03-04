"""
Basic tests for WhisperRoom.
Run from project root: pytest tests/ -v
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test env BEFORE any app imports
os.environ['FLASK_ENV']      = 'testing'
os.environ['DATABASE_URL']   = 'sqlite:///:memory:'
os.environ['SECRET_KEY']     = 'test-secret'
os.environ['ADMIN_PASSWORD'] = 'testpass'

import pytest


@pytest.fixture(scope='function')
def app():
    from app import create_app, db
    flask_app = create_app('testing')
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


# ── Route tests ───────────────────────────────────────────────────────────────

def test_lobby_loads(client):
    r = client.get('/')
    assert r.status_code == 200
    assert b'WhisperRoom' in r.data


def test_create_room(client):
    r = client.post('/create-room', data={'room_name': 'testroom'})
    assert r.status_code == 302
    assert 'testroom' in r.headers['Location']


def test_room_page_loads(client):
    client.post('/create-room', data={'room_name': 'hello'})
    r = client.get('/room/hello')
    assert r.status_code == 200
    assert b'hello' in r.data


def test_missing_room_returns_404(client):
    r = client.get('/room/doesnotexist')
    assert r.status_code == 404


def test_admin_login_page(client):
    r = client.get('/admin/login')
    assert r.status_code == 200


def test_admin_wrong_password(client):
    r = client.post('/admin/login', data={'password': 'wrongpass'})
    assert b'Wrong password' in r.data


def test_admin_correct_password(client):
    r = client.post('/admin/login', data={'password': 'testpass'})
    assert r.status_code == 302


def test_admin_requires_login(client):
    r = client.get('/admin/')
    assert r.status_code == 302
    assert 'login' in r.headers['Location']


def test_search_endpoint(client):
    client.post('/create-room', data={'room_name': 'searchroom'})
    r = client.get('/room/searchroom/search?q=hello')
    assert r.status_code == 200
    data = r.get_json()
    assert 'results' in data
    assert 'count' in data


def test_search_too_short(client):
    client.post('/create-room', data={'room_name': 'searchroom2'})
    r = client.get('/room/searchroom2/search?q=a')
    data = r.get_json()
    assert data['count'] == 0


# ── Model tests ───────────────────────────────────────────────────────────────

def test_room_get_or_create(app):
    from app.models import Room
    with app.app_context():
        r1 = Room.get_or_create('myroom')
        r2 = Room.get_or_create('myroom')
        assert r1.id == r2.id


def test_user_session_persistence(app):
    from app.models import UserSession
    from app.utils import generate_nick, generate_token
    from app import db
    with app.app_context():
        token = generate_token()
        s1 = UserSession.get_or_create(token, generate_nick)
        s2 = UserSession.get_or_create(token, generate_nick)
        assert s1.nick == s2.nick


def test_message_search(app):
    from app.models import Room, Message
    from app import db
    with app.app_context():
        room = Room.get_or_create('searchtest')
        msg  = Message(room_id=room.id, nick='tester', text='hello world')
        db.session.add(msg)
        db.session.commit()
        results = Message.search(room.id, 'hello')
        assert len(results) == 1
        assert results[0].text == 'hello world'


def test_ban_user(app):
    from app.models import UserSession
    from app.utils import generate_nick, generate_token
    from app import db
    with app.app_context():
        token = generate_token()
        s = UserSession.get_or_create(token, generate_nick)
        s.is_banned = True
        db.session.commit()
        reloaded = UserSession.query.filter_by(token=token).first()
        assert reloaded.is_banned is True
