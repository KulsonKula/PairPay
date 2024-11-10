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
    from app.models import user, log
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Usuń istniejących użytkowników przed dodaniem nowych
        db.query(user).delete()  # Usuwa wszystkie rekordy w tabeli user
        db.commit()
        db.query(log).delete()  # Usuwa wszystkie rekordy w tabeli log
        db.commit()

        # Dodaj przykładowe dane
        user1 = user(name="Alice", surname="Smith",
                          mail="alice@gmail.com", password_hash="securepass", admin=True)
        user2 = user(name="Bob", surname="Jones",
                          mail="bob@gmail.com", password_hash="anotherpass")

        db.add(user1)
        db.add(user2)

        log1 = log(user_id=user1.id, data="User logged in",
                   created_at=func.now())
        log2 = log(user_id=user2.id, data="User created a bill",
                   created_at=func.now())
        db.add(log1)
        db.add(log2)

        db.commit()  # Zatwierdzamy zmiany
    except Exception as e:
        db.rollback()
        print(f"Error during DB initialization: {e}")
    finally:
        db.close()
