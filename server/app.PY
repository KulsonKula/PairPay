
import cv2
from PIL import Image
import pytesseract
import os
import ollama
import numpy as np

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*",
     "methods": ["GET", "POST"], "allow_headers": ["Content-Type"]}})
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def procces_img(img):
    image = Image.open(img.stream)
    image_np = np.array(image)

    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    photo = Image.fromarray(binary_image)

    text = pytesseract.image_to_string(photo, lang='pol')
    return text


def use_llm(text):
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'system',
            'content': '''You will be given a recipe summary in Polish, your task is to extract only all items and their prices, ignoring tax and information about transacion.
            Write all information in JSON format. Dont write additional information or comments.
            Each item must be as individual item. Keys: "name", "quantity", "price"
            example:
            "ITEMS":[
        {
            "name": "example item 1",
            "quantity": 2,
            "price": 10.99
        },
        {
            "name": "example item 2",
            "quantity": 1,
            "price": 5.49
        }
    ]''',
        },
        {
            'role': 'user',
            'content': f"{text}",
        },
    ])
    return response['message']['content']


def validate_responce(text):
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': f"If text delimited by triple backticks is in correct JSON formating, if yes return 1, if not return 0, dont give addisional information. \n```{text}```",
        },
    ])

    return response['message']['content']


@ app.route('/upload', methods=['POST'])
def get_items():

    counter = 0
    if 'file' not in request.files:
        return jsonify({"error": "Brak pliku"}), 400

    file = request.files['file']

    try:
        while (counter < 3):
            counter += 1

            img = procces_img(file)
            responce = use_llm(img)
            validation = validate_responce(responce)

            if validation == "1":
                return responce

        return jsonify({"error: bad img"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
