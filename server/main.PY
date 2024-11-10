
import cv2
from PIL import Image
import pytesseract
import os
import ollama
import numpy as np

from flask import Flask, jsonify, request
from app.config_cors import configure_cors
from app.db import init_db

app = Flask(__name__)

# Konfiguracja CORS
configure_cors(app)

init_db()

if __name__ == '__main__':
    app.run(debug=True)
