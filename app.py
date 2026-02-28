from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-in-production'

socketio = SocketIO(app, cors_allowed_origins="*")

# Track connected users: { socket_id: nickname }
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('user_join')
def handle_join(data):
    """Client sends their nickname right after connecting."""
    nick = data.get('nick', 'unknown')
    users[request.sid] = nick
    print(f'[+] {nick} joined  (online: {len(users)})')

    # Notify everyone
    emit('system_message', {'text': f'{nick} joined the room 👋'}, broadcast=True)
    # Push fresh user list to everyone
    emit('user_list', {'users': list(users.values())}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    """Broadcast chat message to all clients."""
    emit('new_message', data, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    nick = users.pop(request.sid, None)
    if nick:
        print(f'[-] {nick} left   (online: {len(users)})')
        emit('system_message', {'text': f'{nick} left the room 👋'}, broadcast=True)
        emit('user_list', {'users': list(users.values())}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
