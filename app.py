"""
Handwritten Text Recognition Web App
======================================
Backend: Flask + pytesseract + OpenCV
Author: Generated for GitHub/Render deployment
"""

import os
import cv2
import numpy as np
import pytesseract
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import base64
import io
from PIL import Image

# ──────────────────────────────────────────────
# App Configuration
# ──────────────────────────────────────────────
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ──────────────────────────────────────────────
# Tesseract Path (adjust for local Windows users)
# On Linux/Render, tesseract is found automatically via PATH
# On Windows, uncomment and set the path below:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# ──────────────────────────────────────────────


def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_bytes):
    """
    Preprocess the image for better OCR accuracy.
    Steps:
      1. Convert to grayscale
      2. Apply Gaussian blur to reduce noise
      3. Apply adaptive thresholding for binarization
      4. Deskew if needed (basic sharpening)
    Returns: processed NumPy image array
    """
    # Decode image bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image. Please upload a valid image file.")

    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 2: Noise reduction with Gaussian blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Step 3: Adaptive thresholding — handles uneven lighting in handwritten images
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Step 4: Morphological dilation to slightly thicken text strokes
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.dilate(thresh, kernel, iterations=1)

    return processed


def extract_text(processed_img):
    """
    Run pytesseract OCR on the preprocessed image.
    Uses --psm 6 (assume a single uniform block of text) for handwriting.
    Returns: extracted text string
    """
    # Tesseract config: OEM 3 = default engine, PSM 6 = block of text
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_img, config=config)
    return text.strip()


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle image upload, process it, and return extracted text.
    Accepts: multipart/form-data with 'image' field
    Returns: JSON { success, text, error }
    """
    # ── Validate request ──
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided.'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected.'}), 400

    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'File type not allowed. Supported: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400

    try:
        # ── Read file bytes ──
        image_bytes = file.read()

        # ── Preprocess with OpenCV ──
        processed_img = preprocess_image(image_bytes)

        # ── Extract text with Tesseract ──
        extracted_text = extract_text(processed_img)

        if not extracted_text:
            extracted_text = "No text could be detected. Try a clearer image with better contrast."

        return jsonify({
            'success': True,
            'text': extracted_text,
            'filename': secure_filename(file.filename)
        })

    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)}), 400
    except pytesseract.TesseractNotFoundError:
        return jsonify({
            'success': False,
            'error': (
                'Tesseract OCR engine not found on this server. '
                'Please ensure Tesseract is installed. '
                'See README.md for deployment instructions.'
            )
        }), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'Processing error: {str(e)}'}), 500


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == '__main__':
    # Development server — Gunicorn is used in production (Render)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
