from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from config import config

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")


def create_app(env='default'):
    app = Flask(__name__)
    app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from .blueprints.main import main_bp
    from .blueprints.chat import chat_bp
    from .blueprints.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)

    from .blueprints import events  # noqa

    return app
