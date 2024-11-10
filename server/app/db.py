from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    import app.models  # Import modeli, aby Base 'widziało' klasy modeli
    Base.metadata.create_all(bind=engine)
