# app/db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Ustawienia bazy danych
DATABASE_URL = "sqlite:///example.db"  # Ścieżka do bazy danych

# Silnik bazy danych
engine = create_engine(DATABASE_URL, echo=True)

# Podstawowa klasa bazowa dla modeli
Base = declarative_base()

# Fabryka sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funkcja inicjalizująca (tworzenie tabel)


def init_db():
    # Opóźniony import, aby uniknąć cyklicznych importów
    from app.models import user, log, group, expense, bill
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Usuń istniejących użytkowników przed dodaniem nowych
        db.query(user).delete()  # Usuwa wszystkie rekordy w tabeli user
        db.commit()
        db.query(log).delete()  # Usuwa wszystkie rekordy w tabeli log
        db.commit()
        db.query(group).delete()  # Usuwa wszystkie rekordy w tabeli group
        db.commit()
        db.query(expense).delete()  # Usuwa wszystkie rekordy w tabeli expense
        db.commit()
        db.query(bill).delete()  # Usuwa wszystkie rekordy w tabeli bill
        db.commit()

        # Dodaj przykładowe dane dla użytkowników
        user1 = user(name="Alice", surname="Smith", mail="alice@gmail.com",
                     password_hash="securepass", admin=True)
        user2 = user(name="Bob", surname="Jones",
                     mail="bob@gmail.com", password_hash="anotherpass")
        db.add(user1)
        db.add(user2)
        db.commit()

        # Dodaj logi
        log1 = log(user_id=user1.id, data="User logged in",
                   created_at=func.now())
        log2 = log(user_id=user2.id, data="User created a bill",
                   created_at=func.now())
        db.add(log1)
        db.add(log2)
        db.commit()

        # Dodaj grupy (one-to-many, lider i członek)
        group1 = group(user_lider=user1.id, user_member=user2.id)
        group2 = group(user_lider=user2.id, user_member=user1.id)
        db.add(group1)
        db.add(group2)
        db.commit()

        # Dodaj wydatki (expense)
        # Przykład waluty: 1 (np. USD)
        expense1 = expense(name="Dinner", currency=1, price=50.0)
        expense2 = expense(name="Taxi", currency=1, price=30.0)
        db.add(expense1)
        db.add(expense2)
        db.commit()

        # Dodaj faktury (bill)
        bill1 = bill(user_creator_id=user1.id, user_added_id=user2.id, expense_id=expense1.id,
                     name="Dinner Bill", label="Food", status=1, total_sum=50.0)
        bill2 = bill(user_creator_id=user2.id, user_added_id=user1.id, expense_id=expense2.id,
                     name="Taxi Bill", label="Transport", status=2, total_sum=30.0)
        db.add(bill1)
        db.add(bill2)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error during DB initialization: {e}")
    finally:
        db.close()
