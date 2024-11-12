from app import db


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_lider = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_member = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False)

    lider = db.relationship(
        "User", back_populates="groups_led", foreign_keys=[user_lider])

    member = db.relationship(
        "User", back_populates="groups_member", foreign_keys=[user_member])

    def to_dict(self):
        return {
            "id": self.id,
            "user_lider": self.user_lider,
            "user_member": self.user_member,
            "created_at": self.created_at
        }
