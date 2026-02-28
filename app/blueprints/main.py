from flask import Blueprint, render_template, redirect, url_for, request, make_response
from ..models import Room, UserSession
from ..utils import generate_nick, generate_token

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Lobby — list all rooms and let user pick or create one."""
    rooms = Room.query.order_by(Room.created_at.desc()).all()

    token = request.cookies.get('wr_token')
    if not token:
        token = generate_token()

    session = UserSession.get_or_create(token, generate_nick)

    resp = make_response(render_template('main/lobby.html', rooms=rooms, nick=session.nick))
    resp.set_cookie('wr_token', token, max_age=60*60*24*30)
    return resp


@main_bp.route('/create-room', methods=['POST'])
def create_room():
    name = request.form.get('room_name', '').strip().lower()
    name = ''.join(c for c in name if c.isalnum() or c in '-_')[:32]
    if name:
        Room.get_or_create(name)
    return redirect(url_for('chat.room', room_name=name))
