"""
Basic tests for WhisperRoom.
Run: pytest tests/ -v
"""
import pytest
import os
os.environ['FLASK_ENV']      = 'testing'
os.environ['DATABASE_URL']   = 'sqlite:///:memory:'
os.environ['SECRET_KEY']     = 'test-secret'
os.environ['ADMIN_PASSWORD'] = 'testpass'

from run import app as flask_app
from app import db as _db


@pytest.fixture
def app():
    flask_app.config['TESTING']   = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ── Route tests ──────────────────────────────────────────────────────────────

def test_lobby_loads(client):
    """Lobby page returns 200."""
    r = client.get('/')
    assert r.status_code == 200
    assert b'WhisperRoom' in r.data


def test_create_room(client):
    """Creating a room redirects to the room page."""
    r = client.post('/create-room', data={'room_name': 'testroom'})
    assert r.status_code == 302
    assert b'testroom' in r.headers['Location'].encode()


def test_room_page_loads(client):
    """Room page loads after creation."""
    client.post('/create-room', data={'room_name': 'hello'})
    r = client.get('/room/hello')
    assert r.status_code == 200
    assert b'hello' in r.data


def test_missing_room_returns_404(client):
    """Non-existent room returns 404."""
    r = client.get('/room/doesnotexist')
    assert r.status_code == 404


def test_admin_login_page(client):
    """Admin login page loads."""
    r = client.get('/admin/login')
    assert r.status_code == 200


def test_admin_wrong_password(client):
    """Wrong admin password shows error."""
    r = client.post('/admin/login', data={'password': 'wrongpass'})
    assert b'Wrong password' in r.data


def test_admin_correct_password(client):
    """Correct admin password redirects to dashboard."""
    r = client.post('/admin/login', data={'password': 'testpass'})
    assert r.status_code == 302


def test_search_endpoint(client):
    """Search endpoint returns JSON."""
    client.post('/create-room', data={'room_name': 'searchroom'})
    r = client.get('/room/searchroom/search?q=hello')
    assert r.status_code == 200
    data = r.get_json()
    assert 'results' in data
    assert 'count' in data


def test_search_too_short(client):
    """Search with 1 char returns empty results."""
    client.post('/create-room', data={'room_name': 'searchroom2'})
    r = client.get('/room/searchroom2/search?q=a')
    data = r.get_json()
    assert data['count'] == 0


# ── Model tests ───────────────────────────────────────────────────────────────

def test_room_get_or_create(app):
    """Room.get_or_create creates then returns same room."""
    from app.models import Room
    with app.app_context():
        r1 = Room.get_or_create('myroom')
        r2 = Room.get_or_create('myroom')
        assert r1.id == r2.id


def test_user_session_persistence(app):
    """UserSession returns same nick for same token."""
    from app.models import UserSession
    from app.utils import generate_nick, generate_token
    with app.app_context():
        token = generate_token()
        s1 = UserSession.get_or_create(token, generate_nick)
        s2 = UserSession.get_or_create(token, generate_nick)
        assert s1.nick == s2.nick


def test_message_search(app):
    """Message.search finds matching messages."""
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
