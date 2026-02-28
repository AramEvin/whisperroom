from datetime import datetime
from .. import db


class UserSession(db.Model):
    __tablename__ = 'user_sessions'

    id         = db.Column(db.Integer, primary_key=True)
    token      = db.Column(db.String(64), unique=True, nullable=False, index=True)
    nick       = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserSession {self.nick}>'

    def to_dict(self):
        return {'token': self.token, 'nick': self.nick}

    @staticmethod
    def get_or_create(token, nick_generator):
        session = UserSession.query.filter_by(token=token).first()
        if not session:
            session = UserSession(token=token, nick=nick_generator())
            db.session.add(session)
            db.session.commit()
        else:
            session.last_seen = datetime.utcnow()
            db.session.commit()
        return session
