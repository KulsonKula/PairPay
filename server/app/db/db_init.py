from flask import current_app
from app.models import Group, User, Log, Expense, Bill
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def init_db():
    db = current_app.db
    engine = db.get_engine()
    Base.metadata.create_all(bind=engine)

    try:
        with db.get_session() as db_session:
            db_session.query(Log).delete()
            db_session.query(Bill).delete()
            db_session.query(Expense).delete()
            db_session.query(Group).delete()
            db_session.query(User).delete()
            db_session.commit()

            user1 = create_user(db_session, "Alice", "Smith",
                                "alice@gmail.com", "securepass", True)
            user2 = create_user(db_session, "Bob", "Jones",
                                "bob@gmail.com", "anotherpass")

            create_log(db_session, user1.id, "User logged in")
            create_log(db_session, user2.id, "User created a bill")

            create_group(db_session, user1.id, user2.id)
            create_group(db_session, user2.id, user1.id)

            expense1 = create_expense(db_session, "Dinner", 1, 50.0)
            expense2 = create_expense(db_session, "Taxi", 1, 30.0)

            create_bill(db_session, user1.id, user2.id,
                        expense1.id, "Dinner Bill", "Food", 1, 50.0)
            create_bill(db_session, user2.id, user1.id, expense2.id,
                        "Taxi Bill", "Transport", 2, 30.0)

    except SQLAlchemyError as e:
        print(f"Error during DB initialization: {e}")
        db_session.rollback()


def create_user(db_session, name, surname, mail, password, admin=False):
    user = User(name=name, surname=surname, mail=mail,
                password_hash=password, admin=admin)
    db_session.add(user)
    db_session.commit()
    return user


def create_log(db_session, user_id, data):
    log = Log(user_id=user_id, data=data, created_at=func.now())
    db_session.add(log)
    db_session.commit()


def create_group(db_session, user_lider, user_member):
    group = Group(user_lider=user_lider, user_member=user_member)
    db_session.add(group)
    db_session.commit()


def create_expense(db_session, name, currency, price):
    expense = Expense(name=name, currency=currency, price=price)
    db_session.add(expense)
    db_session.commit()
    return expense


def create_bill(db_session, user_creator_id, user_added_id, expense_id, name, label, status, total_sum):
    bill = Bill(user_creator_id=user_creator_id, user_added_id=user_added_id, expense_id=expense_id,
                name=name, label=label, status=status, total_sum=total_sum)
    db_session.add(bill)
    db_session.commit()
