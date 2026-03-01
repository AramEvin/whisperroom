from datetime import datetime
from .. import db


class Message(db.Model):
    __tablename__ = 'messages'

    id         = db.Column(db.Integer, primary_key=True)
    room_id    = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False, index=True)
    nick       = db.Column(db.String(64), nullable=False)
    text       = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Message {self.nick}: {self.text[:30]}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nick': self.nick,
            'text': self.text,
            'created_at': self.created_at.strftime('%H:%M'),
            'date': self.created_at.strftime('%Y-%m-%d'),
        }

    @staticmethod
    def search(room_id, query, limit=50):
        """Full-text search in room messages."""
        return (
            Message.query
            .filter(
                Message.room_id == room_id,
                Message.text.ilike(f'%{query}%')
            )
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )
