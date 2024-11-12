from app import db
from app.models import Group, User, Log, Expense, Bill
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


def init_db():
    db.create_all()

    try:
        db.session.query(Log).delete()
        db.session.query(Bill).delete()
        db.session.query(Expense).delete()
        db.session.query(Group).delete()
        db.session.query(User).delete()
        db.session.commit()

        user1 = create_user(
            "Alice", "Smith", "alice@gmail.com", "securepass", True)
        user2 = create_user("Bob", "Jones", "bob@gmail.com", "anotherpass")

        create_log(user1.id, "User logged in")
        create_log(user2.id, "User created a bill")

        create_group(user1.id, user2.id)
        create_group(user2.id, user1.id)

        expense1 = create_expense("Dinner", 1, 50.0)
        expense2 = create_expense("Taxi", 1, 30.0)

        create_bill(user1.id, user2.id, expense1.id,
                    "Dinner Bill", "Food", 1, 50.0)
        create_bill(user2.id, user1.id, expense2.id,
                    "Taxi Bill", "Transport", 2, 30.0)

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error during DB initialization: {e}")


def create_user(name, surname, mail, password, admin=False):
    user = User(name=name, surname=surname, mail=mail,
                password=password, admin=admin)
    db.session.add(user)
    db.session.commit()
    return user


def create_log(user_id, data):
    log = Log(user_id=user_id, data=data, created_at=func.now())
    db.session.add(log)
    db.session.commit()


def create_group(user_lider, user_member):
    group = Group(user_lider=user_lider, user_member=user_member)
    db.session.add(group)
    db.session.commit()


def create_expense(name, currency, price):
    expense = Expense(name=name, currency=currency, price=price)
    db.session.add(expense)
    db.session.commit()
    return expense


def create_bill(user_creator_id, user_added_id, expense_id, name, label, status, total_sum):
    bill = Bill(user_creator_id=user_creator_id, user_added_id=user_added_id,
                expense_id=expense_id, name=name, label=label, status=status, total_sum=total_sum)
    db.session.add(bill)
    db.session.commit()
