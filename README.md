![GitHub repo size](https://img.shields.io/github/repo-size/keerthanad1105-2005/handwritten-text-recognition)
![GitHub stars](https://img.shields.io/github/stars/keerthanad1105-2005/handwritten-text-recognition?style=social)
![GitHub forks](https://img.shields.io/github/forks/keerthanad1105-2005/handwritten-text-recognition?style=social)
![GitHub issues](https://img.shields.io/github/issues/keerthanad1105-2005/handwritten-text-recognition)
![GitHub license](https://img.shields.io/github/license/keerthanad1105-2005/handwritten-text-recognition)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)
![Deployed on Render](https://img.shields.io/badge/Deployed-Render-blueviolet)


# ✍️ Handwritten Text Recognition Web App

A full-stack web application that extracts text from handwritten images using **Tesseract OCR**, **OpenCV**, and **Flask**.

Upload a photo of handwritten notes, letters, or documents — the app processes the image and returns the detected text instantly.

---

## 📸 Features

- 📤 Drag-and-drop or click-to-upload image interface
- 🖼️ Live image preview before submission
- 🔍 OCR powered by Tesseract via `pytesseract`
- 🧠 Image preprocessing with OpenCV (grayscale → blur → adaptive thresholding)
- 📋 Copy result to clipboard
- 💾 Download extracted text as `.txt`
- 📱 Fully responsive, mobile-friendly UI
- 🚀 Ready to deploy on **Render** (free tier)

---

## 🗂️ Project Structure

```
handwritten-text-recognition/
│── app.py               # Flask backend (routes + OCR logic)
│── requirements.txt     # Python dependencies
│── runtime.txt          # Python version for Render
│── render.yaml          # Render deployment config
│── README.md            # You are here
│── static/
│   └── style.css        # Stylesheet
└── templates/
    └── index.html       # Frontend UI
```

---

## 🖥️ Local Setup

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | [python.org](https://python.org) |
| Tesseract OCR | 4.x or 5.x | See below |
| pip | latest | bundled with Python |

---

### 1️⃣ Install Tesseract OCR (System Package)

> ⚠️ **Important:** `pytesseract` is just a Python wrapper. You must install the actual Tesseract binary on your system.

**Ubuntu / Debian / WSL:**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng -y
```

**macOS (Homebrew):**
```bash
brew install tesseract
```

**Windows:**
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it (default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`)
3. Uncomment and update this line in `app.py`:
```python
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

Verify installation:
```bash
tesseract --version
```

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/handwritten-text-recognition.git
cd handwritten-text-recognition
```

---

### 3️⃣ Create a Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

---

### 4️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Run the App

```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## 🐙 Upload to GitHub

### First time:

```bash
# 1. Initialize git
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit: Handwritten Text Recognition App"

# 4. Create repo on GitHub (github.com → New Repository)
#    Name it: handwritten-text-recognition
#    Leave it empty (no README, no .gitignore)

# 5. Link and push
git remote add origin https://github.com/YOUR_USERNAME/handwritten-text-recognition.git
git branch -M main
git push -u origin main
```

### Subsequent updates:

```bash
git add .
git commit -m "Your change description"
git push
```

---

## 🚀 Deploy on Render (Free)

Render is a cloud platform with a **free tier** that supports Python web services.

### Step 1 — Sign up / log in

Go to: https://render.com and connect your GitHub account.

### Step 2 — Create a new Web Service

1. Click **New → Web Service**
2. Connect your **GitHub repository**
3. Render will auto-detect `render.yaml` — click **Apply**

### Step 3 — Configure (if setting manually)

| Field | Value |
|-------|-------|
| **Runtime** | Python 3 |
| **Build Command** | `apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng libgl1-mesa-glx && pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT --timeout 120` |
| **Plan** | Free |

### Step 4 — Deploy

Click **Create Web Service**. Render will:
1. Pull your code from GitHub
2. Install Tesseract as a system package
3. Install Python dependencies
4. Start Gunicorn

Your app will be live at: `https://handwritten-text-recognition.onrender.com`

---

## ⚙️ Tesseract on Render — How It Works

Render runs on Ubuntu. The `buildCommand` in `render.yaml` installs Tesseract directly:

```bash
apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng libgl1-mesa-glx
```

- `tesseract-ocr` — the OCR engine binary
- `tesseract-ocr-eng` — English language data
- `libgl1-mesa-glx` — required by OpenCV on headless servers

> 💡 For other languages (e.g., Hindi), add `tesseract-ocr-hin` to the install command.

---

## 🔧 API Reference

### `GET /`
Returns the main HTML page.

### `POST /predict`
Processes an uploaded image and returns extracted text.

**Request:** `multipart/form-data`
| Field | Type | Description |
|-------|------|-------------|
| `image` | file | Image file (PNG, JPG, BMP, TIFF, WebP) |

**Response:** `application/json`
```json
{
  "success": true,
  "text": "Hello world this is handwritten",
  "filename": "notes.jpg"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `flask` | Web framework |
| `gunicorn` | WSGI production server |
| `pytesseract` | Python wrapper for Tesseract OCR |
| `opencv-python-headless` | Image processing (no GUI) |
| `Pillow` | Image handling |
| `numpy` | Array operations for OpenCV |

---

## 🧠 How OCR Works (Pipeline)

```
Upload Image
    ↓
Read bytes → NumPy array (OpenCV)
    ↓
Convert to Grayscale
    ↓
Gaussian Blur (noise reduction)
    ↓
Adaptive Thresholding (binarize)
    ↓
Morphological Dilation (thicken strokes)
    ↓
Tesseract OCR (--oem 3 --psm 6)
    ↓
Return extracted text
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `TesseractNotFoundError` | Install Tesseract binary (see Step 1) |
| Blank output | Try a higher-contrast image; crop to text area |
| `libGL.so.1` missing | Run `apt install libgl1-mesa-glx` |
| Render build fails | Check build logs; ensure `apt-get` commands run without sudo on Render |
| Wrong language | Install `tesseract-ocr-<lang>` and pass `lang='<code>'` to `image_to_string` |

---

## 📝 License

MIT License — free to use, modify, and deploy.

---

## 🙏 Acknowledgements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) by Google
- [OpenCV](https://opencv.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Render](https://render.com/) for free hosting

##AUTHOR

-KEERTHANA D

#### 🚀 Live Demo
Try the deployed project here:  
👉  https://handwritten-text-recognition-3.onrender.com/
