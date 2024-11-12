from app import db
from sqlalchemy_utils import EmailType


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    mail = db.Column(EmailType, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    bills_created = db.relationship(
        "Bill", foreign_keys="[Bill.user_creator_id]", back_populates="user_creator"
    )
    bills_added = db.relationship(
        "Bill", foreign_keys="[Bill.user_added_id]", back_populates="user_added"
    )

    groups_led = db.relationship(
        "Group", back_populates="lider", foreign_keys="[Group.user_lider]"
    )

    groups_member = db.relationship(
        "Group", back_populates="member", foreign_keys="[Group.user_member]"
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
