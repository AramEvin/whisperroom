from datetime import datetime
from .. import db


class Room(db.Model):
    __tablename__ = 'rooms'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(32), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages   = db.relationship('Message', backref='room', lazy='dynamic',
                                 cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Room {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'message_count': self.messages.count(),
        }

    @staticmethod
    def get_or_create(name):
        room = Room.query.filter_by(name=name).first()
        if not room:
            room = Room(name=name)
            db.session.add(room)
            db.session.commit()
        return room
