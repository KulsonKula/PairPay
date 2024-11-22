from sqlalchemy import or_
from app.models import Bill, bill_user, Invitation
from app import db


def get_bills_for_user_creator(user_id):
    return (
        Bill.query.outerjoin(bill_user)
        .filter(Bill.user_creator_id == user_id)
        .distinct()
        .all()
    )


def get_bills_for_user_assigned(user_id):
    return (
        Bill.query.outerjoin(bill_user)
        .filter(bill_user.c.user_id == user_id)
        .distinct()
        .all()
    )


def get_bill_for_user(bill_id, current_user):
    bill = Bill.query.filter(
        Bill.id == bill_id,
        (Bill.user_creator_id == current_user) | (Bill.users.any(id=current_user)),
    ).first()

    return bill


def update_bill_fields(bill, bill_data):
    updatable_fields = ["name", "label", "status", "total_sum"]
    for field in updatable_fields:
        if field in bill_data:
            setattr(bill, field, bill_data[field])


# def update_bill_users(bill, new_user_ids):
#     if not new_user_ids:
#         return

#     current_user_ids = {user.id for user in bill.users}
#     new_user_ids = set(new_user_ids)

#     users_to_add = new_user_ids - current_user_ids
#     users_to_remove = current_user_ids - new_user_ids

#     if users_to_add:
#         new_users = User.query.filter(User.id.in_(users_to_add)).all()
#         for user in new_users:
#             if user not in bill.users:
#                 bill.users.append(user)

#     if users_to_remove:
#         users_to_remove_objs = User.query.filter(
#             User.id.in_(users_to_remove)).all()
#         for user in users_to_remove_objs:
#             if user in bill.users:
#                 bill.users.remove(user)


def delete_bill(bill_id, current_user):
    bill = Bill.query.filter_by(id=bill_id, user_creator_id=current_user).first()

    if not bill:
        return None, "Bill not found or user does not have access"

    db.session.delete(bill)
    db.session.commit()

    return bill


def invite_user_to_bill(bill_id, current_user, invitee_id):
    bill = Bill.query.filter_by(id=bill_id, user_creator_id=current_user).first()

    if not bill:
        raise PermissionError("Only creator of the bill can invite users")

    if any(user.id == invitee_id for user in bill.users):
        raise ValueError("User is already part of the bill")

    invitation = Invitation(
        inviter_id=current_user, invitee_id=invitee_id, bill_id=bill_id
    )

    db.session.add(invitation)
    db.session.commit()

    return invitation
