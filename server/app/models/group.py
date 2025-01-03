from app import db
from sqlalchemy.dialects.postgresql import UUID

user_group = db.Table(
    "user_group",
    db.Column(
        "user_id", UUID(as_uuid=True), db.ForeignKey("user.id"), primary_key=True
    ),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"), primary_key=True),
)


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_lider = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    lider = db.relationship(
        "User", back_populates="groups_led", foreign_keys=[user_lider]
    )

    members = db.relationship(
        "User", secondary="user_group", back_populates="member_of_groups", cascade="all"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_lider": self.user_lider,
            "created_at": self.created_at,
        }
