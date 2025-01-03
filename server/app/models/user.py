from app import db
from sqlalchemy_utils import EmailType
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    mail = db.Column(EmailType, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    is_activated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    bills_created = db.relationship(
        "Bill", foreign_keys="[Bill.user_creator_id]", back_populates="user_creator"
    )

    bills = db.relationship("Bill", secondary="bill_user", back_populates="users")
    expense_participants = db.relationship("ExpenseParticipant", back_populates="user")

    groups_led = db.relationship(
        "Group", back_populates="lider", foreign_keys="[Group.user_lider]"
    )

    member_of_groups = db.relationship(
        "Group", secondary="user_group", back_populates="members"
    )

    log = db.relationship("Log", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "mail": self.mail,
            "admin": self.admin,
            "created_at": self.created_at,
        }
