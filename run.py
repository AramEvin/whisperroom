import os
from app import create_app, socketio, db

env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

# This block only runs in development (python run.py)
# In production gunicorn imports run:app directly
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('✅ Database ready')

        from app.models import Room
        Room.get_or_create('general')
        print('✅ Default room "general" ready')

    print(f'🚀 Starting in {env} mode')
    socketio.run(app, host='0.0.0.0', port=5000, debug=(env == 'development'))
