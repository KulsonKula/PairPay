from app import db
from sqlalchemy.sql import func
import enum
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID


class InvitationStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class Invitation(db.Model):
    __tablename__ = "invitation"

    id = db.Column(db.Integer, primary_key=True)
    inviter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    invitee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey("bill.id"), nullable=False)
    status = db.Column(
        Enum(InvitationStatus), default=InvitationStatus.PENDING, nullable=False
    )
    created_at = db.Column(db.DateTime, server_default=func.now())
