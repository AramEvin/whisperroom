from time import time
from flask import request
from flask_socketio import emit, join_room, disconnect
from .. import socketio, db
from ..models import Room, Message, UserSession, RoomMembership

# ── In-memory state ────────────────────────────────────────────────────────
# { room_name: { sid: nick } }
rooms_online = {}

# Rate limiting: { sid: [timestamp, timestamp, ...] }
message_log = {}

# Config
RATE_LIMIT     = 5    # max messages
RATE_WINDOW    = 10   # per N seconds


def get_room_users(room_name):
    return list(rooms_online.get(room_name, {}).values())


def get_online_counts():
    """Return { room_name: count } for all rooms with users."""
    return {r: len(u) for r, u in rooms_online.items() if u}


def is_banned(token):
    if not token:
        return False
    s = UserSession.query.filter_by(token=token).first()
    return s.is_banned if s else False


def is_rate_limited(sid):
    """Return True if this sid has sent too many messages recently."""
    now = time()
    timestamps = message_log.get(sid, [])
    # Keep only timestamps within the window
    timestamps = [t for t in timestamps if now - t < RATE_WINDOW]
    message_log[sid] = timestamps

    if len(timestamps) >= RATE_LIMIT:
        return True

    timestamps.append(now)
    message_log[sid] = timestamps
    return False


# ── Socket events ──────────────────────────────────────────────────────────

@socketio.on('join')
def on_join(data):
    room_name = data.get('room')
    nick      = data.get('nick', 'unknown')
    token     = data.get('token', '')

    if not room_name:
        return

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

    # Broadcast updated live counts to lobby
    emit('online_counts', get_online_counts(), broadcast=True)

    print(f'[JOIN]  {nick} → #{room_name} | Online: {len(rooms_online[room_name])}')


@socketio.on('disconnect')
def on_disconnect():
    message_log.pop(request.sid, None)

    for room_name, users in list(rooms_online.items()):
        if request.sid in users:
            nick = users.pop(request.sid)
            emit('user_left', {'nick': nick}, to=room_name)
            emit('user_list', {'users': get_room_users(room_name)}, to=room_name)

            # Broadcast updated live counts to lobby
            emit('online_counts', get_online_counts(), broadcast=True)

            print(f'[LEAVE] {nick} ← #{room_name} | Online: {len(users)}')


@socketio.on('send_message')
def on_message(data):
    room_name = data.get('room')
    nick      = data.get('nick', 'unknown')
    text      = data.get('text', '').strip()
    token     = data.get('token', '')

    if not room_name or not text or len(text) > 500:
        return

    if is_banned(token):
        emit('banned', {'message': 'You have been banned.'})
        return

    # ── Rate limit check ──
    if is_rate_limited(request.sid):
        emit('rate_limited', {
            'message': f'Slow down — max {RATE_LIMIT} messages per {RATE_WINDOW} seconds.'
        })
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


@socketio.on('lobby_join')
def on_lobby_join():
    """Client on lobby page subscribes to live counts."""
    join_room('__lobby__')
    emit('online_counts', get_online_counts())
