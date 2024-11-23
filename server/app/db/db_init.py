from logging import getLogger
from app import db
from app.models import (
    Group,
    User,
    Split,
    Log,
    Expense,
    Bill,
    user_group,
    bill_user,
    Friendship,
    bill_expense,
    Invitation,
    InvitationStatus,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

logger = getLogger(__name__)


def init_db():
    db.create_all()

    try:
        db.session.execute(user_group.delete())
        db.session.execute(bill_user.delete())
        db.session.execute(bill_expense.delete())

        db.session.query(Log).delete()
        db.session.query(Invitation).delete()
        db.session.query(Bill).delete()
        db.session.query(Split).delete()
        db.session.query(Expense).delete()
        db.session.query(Group).delete()
        db.session.query(Friendship).delete()
        db.session.query(User).delete()
        db.session.commit()

        user1 = create_user(
            "Alice",
            "Smith",
            "alice@gmail.com",
            generate_password_hash("securepass"),
            True,
        )
        user2 = create_user(
            "Bob", "Jones", "bob@gmail.com", generate_password_hash(
                "anotherpass")
        )
        user3 = create_user(
            "Charlie",
            "Brown",
            "charlie@gmail.com",
            generate_password_hash("password123"),
        )
        user4 = create_user(
            "David", "Miller", "david@gmail.com", generate_password_hash(
                "pass456")
        )
        user5 = create_user(
            "Emma", "Wilson", "emma@gmail.com", generate_password_hash(
                "pass789")
        )
        user6 = create_user(
            "Fiona", "Taylor", "fiona@gmail.com", generate_password_hash(
                "secure123")
        )

        create_log(user4.id, "User signed up")
        create_log(user5.id, "User signed up")
        create_log(user6.id, "User signed up")

        create_friendship(user1.id, user4.id)
        create_friendship(user2.id, user5.id)
        create_friendship(user3.id, user6.id)
        create_friendship(user4.id, user5.id)
        create_friendship(user5.id, user6.id)

        group1 = create_group(user1.id)
        group2 = create_group(user2.id)

        add_user_to_group(group1, user1)
        add_user_to_group(group1, user2)
        add_user_to_group(group2, user2)
        add_user_to_group(group2, user3)

        expense1 = create_expense("Dinner", 1, 50.0)
        expense2 = create_expense("Taxi", 1, 30.0)

        create_bill(
            user1.id,
            [user2.id, user3.id],
            [expense1.id],
            "Dinner Bill",
            "Food",
            1,
            50.0,
        )
        create_bill(
            user2.id, [user1.id], [
                expense2.id], "Taxi Bill", "Transport", 2, 30.0
        )
        create_bill(
            user1.id,
            [user2.id, user3.id],
            [expense1.id],
            "Dinner Bill",
            "Food",
            1,
            50.0,
        )
        create_bill(
            user2.id, [user1.id], [
                expense2.id], "Taxi Bill", "Transport", 2, 30.0
        )

        create_split(expense1.id, user1.id, 30)
        create_split(expense1.id, user2.id, 40)

        logger.info("Database initialization successful.")

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error during DB initialization: {e}")


def create_user(name, surname, mail, password, admin=False):
    user = User(name=name, surname=surname, mail=mail,
                password=password, admin=admin)
    user = User(name=name, surname=surname, mail=mail,
                password=password, admin=admin)
    db.session.add(user)
    db.session.commit()
    logger.info(f"User created: {user.name} {user.surname}")
    return user


def create_log(user_id, data):
    log = Log(user_id=user_id, data=data, created_at=func.now())
    db.session.add(log)
    db.session.commit()
    logger.info(f"Log created for user_id {user_id}: {data}")


def create_group(user_lider):
    group = Group(user_lider=user_lider)
    db.session.add(group)
    db.session.commit()
    logger.info(f"Group created with lider user_id {user_lider}")
    return group


def add_user_to_group(group, user):
    if user not in group.members:
        group.members.append(user)
        db.session.commit()
        logger.info(f"User {user.id} added to Group {group.id}")
    else:
        logger.info(f"User {user.id} already in Group {group.id}")


def create_expense(name, currency, price):
    expense = Expense(name=name, currency=currency, price=price)
    db.session.add(expense)
    db.session.commit()
    logger.info(f"Expense created: {name}, Price: {price}")
    return expense


def create_split(expense_id, user_id, split_amount):
    split = Split(expense_id=expense_id, user_id=user_id,
                  split_amount=split_amount)
    split = Split(expense_id=expense_id, user_id=user_id,
                  split_amount=split_amount)
    db.session.add(split)
    db.session.commit()
    logger.info(f"Split created: {expense_id}, Price: {split_amount}")
    return split


def create_bill(
    user_creator_id, user_added_ids, expense_ids, name, label, status, total_sum
):
    bill = Bill(
        user_creator_id=user_creator_id,
        name=name,
        label=label,
        status=status,
        total_sum=total_sum,
        total_sum=total_sum,
    )
    db.session.add(bill)
    db.session.commit()

    for user_id in user_added_ids:
        user = User.query.get(user_id)
        if user:
            bill.users.append(user)

    for expense_id in expense_ids:
        expense = Expense.query.get(expense_id)
        if expense:
            bill.expenses.append(expense)

    db.session.commit()
    logger.info(
        f"Bill created: {name}, Total Sum: {total_sum}, Users: {
            user_added_ids}, Expenses: {expense_ids}"
    )


def create_friendship(user_id_1, user_id_2):
    """Creates a friendship between two users."""
    friendship = Friendship(
        user_id=user_id_1, friend_id=user_id_2, status=InvitationStatus.ACCEPTED
    )
    db.session.add(friendship)
    db.session.commit()
    logger.info(
        f"Friendship {friendship.id} created between user {
            user_id_1} and user {user_id_2}"
    )
