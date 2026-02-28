from flask import request
from flask_socketio import emit, join_room, disconnect
from .. import socketio, db
from ..models import Room, Message, UserSession

# In-memory: { room_name: { sid: nick } }
rooms_online = {}


def get_room_users(room_name):
    return list(rooms_online.get(room_name, {}).values())


def is_banned(token):
    if not token:
        return False
    s = UserSession.query.filter_by(token=token).first()
    return s.is_banned if s else False


@socketio.on('join')
def on_join(data):
    room_name = data.get('room')
    nick      = data.get('nick', 'unknown')
    token     = data.get('token', '')

    if not room_name:
        return

    # Kick banned users immediately
    if is_banned(token):
        emit('banned', {'message': 'You have been banned from WhisperRoom.'})
        disconnect()
        return

    join_room(room_name)

    if room_name not in rooms_online:
        rooms_online[room_name] = {}
    rooms_online[room_name][request.sid] = nick

    emit('user_joined', {'nick': nick}, to=room_name)
    emit('user_list', {'users': get_room_users(room_name)}, to=room_name)
    print(f'[JOIN]  {nick} → #{room_name} | Online: {len(rooms_online[room_name])}')


@socketio.on('disconnect')
def on_disconnect():
    for room_name, users in list(rooms_online.items()):
        if request.sid in users:
            nick = users.pop(request.sid)
            emit('user_left', {'nick': nick}, to=room_name)
            emit('user_list', {'users': get_room_users(room_name)}, to=room_name)
            print(f'[LEAVE] {nick} ← #{room_name} | Online: {len(users)}')


@socketio.on('send_message')
def on_message(data):
    room_name = data.get('room')
    nick      = data.get('nick', 'unknown')
    text      = data.get('text', '').strip()
    token     = data.get('token', '')

    if not room_name or not text or len(text) > 500:
        return

    # Silently block banned users
    if is_banned(token):
        emit('banned', {'message': 'You have been banned from WhisperRoom.'})
        return

    room = Room.query.filter_by(name=room_name).first()
    if not room:
        return

    msg = Message(room_id=room.id, nick=nick, text=text)
    db.session.add(msg)
    db.session.commit()

    emit('new_message', msg.to_dict(), to=room_name)


@socketio.on('typing')
def on_typing(data):
    room_name = data.get('room')
    if room_name:
        emit('user_typing', data, to=room_name, include_self=False)
