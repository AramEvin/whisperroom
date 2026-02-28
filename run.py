import os
from app import create_app, socketio, db

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()           # create tables if they don't exist
        print('✅ Database ready')

        # Seed a default room
        from app.models import Room
        Room.get_or_create('general')
        print('✅ Default room "general" ready')

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
