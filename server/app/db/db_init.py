from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .db_config import engine, Base, SessionLocal
from app.models import Group, User, Log, Expense, Bill


def init_db():
    Base.metadata.create_all(bind=engine)

    try:
        with SessionLocal() as db:
            db.query(Log).delete()
            db.query(Bill).delete()
            db.query(Expense).delete()
            db.query(Group).delete()
            db.query(User).delete()
            db.commit()

            user1 = create_user(db, name="Alice", surname="Smith",
                                mail="alice@gmail.com", password="securepass", admin=True)
            user2 = create_user(db, name="Bob", surname="Jones",
                                mail="bob@gmail.com", password="anotherpass")

            create_log(db, user_id=user1.id, data="User logged in")
            create_log(db, user_id=user2.id, data="User created a bill")

            create_group(db, user_lider=user1.id, user_member=user2.id)
            create_group(db, user_lider=user2.id, user_member=user1.id)

            expense1 = create_expense(
                db, name="Dinner", currency=1, price=50.0)
            expense2 = create_expense(db, name="Taxi", currency=1, price=30.0)

            create_bill(db, user_creator_id=user1.id, user_added_id=user2.id,
                        expense_id=expense1.id, name="Dinner Bill", label="Food", status=1, total_sum=50.0)
            create_bill(db, user_creator_id=user2.id, user_added_id=user1.id, expense_id=expense2.id,
                        name="Taxi Bill", label="Transport", status=2, total_sum=30.0)

    except SQLAlchemyError as e:
        print(f"Error during DB initialization: {e}")
        db.rollback()


def create_user(db: Session, name: str, surname: str, mail: str, password: str, admin: bool = False):
    user = User(name=name, surname=surname, mail=mail,
                password_hash=password, admin=admin)
    db.add(user)
    db.commit()
    return user


def create_log(db: Session, user_id: int, data: str):
    log = Log(user_id=user_id, data=data, created_at=func.now())
    db.add(log)
    db.commit()


def create_group(db: Session, user_lider: int, user_member: int):
    group = Group(user_lider=user_lider, user_member=user_member)
    db.add(group)
    db.commit()


def create_expense(db: Session, name: str, currency: int, price: float):
    expense = Expense(name=name, currency=currency, price=price)
    db.add(expense)
    db.commit()
    return expense


def create_bill(db: Session, user_creator_id: int, user_added_id: int, expense_id: int, name: str, label: str, status: int, total_sum: float):
    bill = Bill(user_creator_id=user_creator_id, user_added_id=user_added_id,
                expense_id=expense_id, name=name, label=label, status=status, total_sum=total_sum)
    db.add(bill)
    db.commit()
