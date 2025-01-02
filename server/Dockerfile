FROM python:3.12-slim

WORKDIR /app

COPY . /app

# Instalacja wymaganych pakietów systemowych (w tym PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalacja zależności Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Ustawienie zmiennych środowiskowych dla Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Uruchomienie aplikacji Flask
CMD ["flask", "run"]
