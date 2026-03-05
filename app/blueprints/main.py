from flask import (Blueprint, render_template, redirect, url_for,
                   request, make_response, session)
from ..models import Room, UserSession, RoomMembership
from ..utils import generate_nick, generate_token
from .. import db

main_bp = Blueprint('main', __name__)


def _get_or_make_session(request):
    token = request.cookies.get('wr_token')
    if not token:
        token = generate_token()
    user = UserSession.get_or_create(token, generate_nick)
    return token, user


@main_bp.route('/')
def index():
    rooms = Room.query.order_by(Room.created_at.desc()).all()
    token, user = _get_or_make_session(request)
    resp = make_response(render_template('main/lobby.html', rooms=rooms, nick=user.nick))
    resp.set_cookie('wr_token', token, max_age=60*60*24*30)
    return resp


@main_bp.route('/create-room', methods=['POST'])
def create_room():
    name = request.form.get('room_name', '').strip().lower()
    name = ''.join(c for c in name if c.isalnum() or c in '-_')[:32]
    if not name:
        return redirect(url_for('main.index'))

    token, user = _get_or_make_session(request)
    room = Room.query.filter_by(name=name).first()

    if not room:
        # New room — creator becomes owner
        room = Room(name=name)
        db.session.add(room)
        db.session.commit()
        RoomMembership.join(room, user, role='owner')
    else:
        # Existing room — join as member if not already
        existing = RoomMembership.get(room.id, user.id)
        if not existing:
            RoomMembership.join(room, user, role='member')

    resp = make_response(redirect(url_for('chat.room', room_name=name)))
    resp.set_cookie('wr_token', token, max_age=60*60*24*30)
    return resp
