# PairPay

## Technologie
[![Python]][python-url]
![flask]
![jwt]
![postgres]
## Opis
Ten projekt implementuje aplikację po stronie serwera, zaprojektowaną do obsługi aplikacji internetowej do podziału kosztów grupowych zakupów.

## Instrukcja instalacji

1. **Klonowanie repozytorium**:
   ```bash
   git clone https://github.com/KulsonKula/PairPay
   cd PairPay
   ```

2. **Instalacja zależności**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Uruchomienie aplikacji**:
   ```bash
   python main.py
   ```

Aby skonfigurować za pomocą Dockera:
1. Zbuduj obraz dockera:
   ```bash
   docker build -t server-app .
   ```
2. Uruchom kontener:
   ```bash
   docker run -p 8000:8000 server-app
   ```

## Architekura
The project has the following structure:
- `app/`: Logika aplikacji i jej konfiguracja
- `requirements.txt`: wymagania Pythonowe
- `Dockerfile`: Konfiguracja dockera

## Autorzy
- Jakub Kula
- Paweł Wójtowicz
- Natalia Stręk
  
[python]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[python-url]: https://www.python.org/

[flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white

[postgres]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white

[jwt]: https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white
