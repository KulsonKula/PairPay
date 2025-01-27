# PairPay

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
  
