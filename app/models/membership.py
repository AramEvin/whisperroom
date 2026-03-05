from datetime import datetime
from .. import db


class RoomMembership(db.Model):
    __tablename__ = 'room_memberships'

    id         = db.Column(db.Integer, primary_key=True)
    room_id    = db.Column(db.Integer, db.ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('user_sessions.id', ondelete='CASCADE'), nullable=False)
    role       = db.Column(db.String(16), nullable=False, default='member')  # 'owner' or 'member'
    joined_at  = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('room_id', 'session_id', name='uq_room_session'),
    )

    room    = db.relationship('Room',        backref=db.backref('memberships', cascade='all, delete-orphan'))
    session = db.relationship('UserSession', backref=db.backref('memberships', cascade='all, delete-orphan'))

    @property
    def is_owner(self):
        return self.role == 'owner'

    def to_dict(self):
        return {
            'nick':      self.session.nick,
            'role':      self.role,
            'is_owner':  self.is_owner,
            'joined_at': self.joined_at.strftime('%Y-%m-%d %H:%M'),
        }

    @staticmethod
    def get(room_id, session_id):
        return RoomMembership.query.filter_by(
            room_id=room_id, session_id=session_id
        ).first()

    @staticmethod
    def join(room, user_session, role='member'):
        existing = RoomMembership.get(room.id, user_session.id)
        if existing:
            return existing
        m = RoomMembership(room_id=room.id, session_id=user_session.id, role=role)
        db.session.add(m)
        db.session.commit()
        return m

    @staticmethod
    def leave(room, user_session):
        m = RoomMembership.get(room.id, user_session.id)
        if m:
            db.session.delete(m)
            db.session.commit()
            return True
        return False
