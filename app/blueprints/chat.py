from flask import Blueprint, render_template, request, make_response, jsonify
from ..models import Room, UserSession, Message
from ..utils import generate_nick, generate_token
from config import Config

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/room/<room_name>')
def room(room_name):
    """Individual chat room page."""
    chat_room = Room.query.filter_by(name=room_name).first_or_404()

    messages = (
        chat_room.messages
        .order_by('created_at')
        .limit(Config.MESSAGE_HISTORY_LIMIT)
        .all()
    )

    token = request.cookies.get('wr_token')
    if not token:
        token = generate_token()
    session = UserSession.get_or_create(token, generate_nick)

    resp = make_response(render_template(
        'chat/room.html',
        room=chat_room,
        history=messages,
        nick=session.nick,
    ))
    resp.set_cookie('wr_token', token, max_age=60*60*24*30)
    return resp


@chat_bp.route('/room/<room_name>/search')
def search(room_name):
    """JSON search endpoint — GET /room/<name>/search?q=hello"""
    chat_room = Room.query.filter_by(name=room_name).first_or_404()
    query = request.args.get('q', '').strip()

    if not query or len(query) < 2:
        return jsonify({'results': [], 'query': query, 'count': 0})

    results = Message.search(chat_room.id, query, limit=30)
    return jsonify({
        'query': query,
        'count': len(results),
        'results': [m.to_dict() for m in results],
    })
