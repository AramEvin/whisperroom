from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-in-production'

socketio = SocketIO(app, cors_allowed_origins="*")

# Track connected users: { session_id: nickname }
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'[CONNECT] sid={request.sid}')

@socketio.on('user_join')
def handle_join(data):
    nick = data.get('nick', 'unknown')
    users[request.sid] = nick
    emit('user_joined', {'nick': nick}, broadcast=True)
    emit('user_list', {'users': list(users.values())}, broadcast=True)
    print(f'[JOIN]  {nick} | Online: {len(users)}')

@socketio.on('disconnect')
def handle_disconnect():
    nick = users.pop(request.sid, None)
    if nick:
        emit('user_left', {'nick': nick}, broadcast=True)
        emit('user_list', {'users': list(users.values())}, broadcast=True)
        print(f'[LEAVE] {nick} | Online: {len(users)}')

@socketio.on('send_message')
def handle_message(data):
    emit('new_message', data, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    # Broadcast typing status to everyone except sender
    emit('user_typing', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
