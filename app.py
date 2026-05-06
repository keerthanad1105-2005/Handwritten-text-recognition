from flask import Flask, render_template, request
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extract_text(image_path):
    url = "https://api.ocr.space/parse/image"

    payload = {
        'apikey': 'helloworld',
        'language': 'eng'
    }

    with open(image_path, 'rb') as f:
        response = requests.post(url, files={'file': f}, data=payload)

    result = response.json()

    try:
        return result['ParsedResults'][0]['ParsedText']
    except:
        return "Error extracting text"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)

    text = extract_text(filepath)

    return text


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
