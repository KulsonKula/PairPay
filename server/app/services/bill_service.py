from sqlalchemy import or_
from app.models import Bill, bill_user


def get_bills_for_user(user_id):
    return (
        Bill.query
        .outerjoin(bill_user)
        .filter(
            or_(
                bill_user.c.user_id == user_id,
                Bill.user_creator_id == user_id
            )
        )
        .distinct()
        .all()
    )
