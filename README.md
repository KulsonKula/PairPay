# PairPay

## Description
This project implements a server-side application designed to handle a web application for splitting the costs of group shopping.

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

To set up with Docker:
1. Build the Docker image:
   ```bash
   docker build -t server-app .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 server-app
   ```

## Architecture
The project has the following structure:
- `app/`: Contains the application logic and configurations
- `doc/`: Documentation files
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker configuration

## Authors
- Jakub Kula
- Paweł Wójtowicz
- Natalia Stręk
  
