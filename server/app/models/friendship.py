from sqlalchemy import Enum
from app import db
from .invitation import InvitationStatus
from sqlalchemy.dialects.postgresql import UUID


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(Enum(InvitationStatus), default=InvitationStatus.PENDING)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref=db.backref("friendships", lazy="dynamic"),
    )
    friend = db.relationship(
        "User",
        foreign_keys=[friend_id],
        backref=db.backref("friend_requests", lazy="dynamic"),
    )
