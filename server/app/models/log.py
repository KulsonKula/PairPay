from app import db


class Log(db.Model):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", back_populates="log")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "data": self.data,
            "created_at": self.created_at,
        }
