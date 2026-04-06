# Phishing Detection System

An advanced, real-time Phishing Detection System powered by Machine Learning and Ensemble techniques. This system evaluates URLs and webpage contents in real-time, leveraging visual heuristics, structural signatures, and lexical analysis to identify cyber threats.

---

## 🚀 Architecture Overview

The project is divided into an inference backend and a modern web interface frontend.

### Backend (FastAPI + Scikit-Learn)
A lightweight and extremely fast Python inference engine.
- **`app.py`**: The application entry point for the FastAPI server.
- **`api/`**: The RESTful endpoints (e.g. `/api/detect`) and strict Pydantic schemas validating inputs/outputs.
- **`security.py`**: Standard API authentication and rate-limiting features.
- **`extractors/`**: The intelligence pipelines extracting deep features from URLs and scraped HTML documents. Includes URL parsing, web element composition (Forms, iframes), and a visual similarity heuristic pipeline.
- **`ml/`**: Machine Learning pipeline for training and serializing the Ensemble model (Random Forest / Gradient Boosted Trees) via `joblib`.

### Frontend (React + Vite)
A cutting-edge UI with glassmorphism effects, a sleek dark mode, and dynamic micro-animations indicating threat analysis phases to the user.

---

## ⚙️ Getting Started

### 1. Prerequisite Setup
Ensure you have Python 3.9+ and Node.js installed.

### 2. Backend Initialization
Install the Python dependencies.

```bash
cd backend
pip install -r requirements.txt
```

### 3. Training the Model
Before running the API, you need to train the machine learning model using the mock dataset provided.

```bash
# Generate the mock data (If not already generated)
python data/generate_mock_data.py

# Train and serialize the model
python backend/ml/train.py
```

*Note: The model artifacts will automatically be saved into `backend/ml/saved_models/`.*

### 4. Running the API
Start the FastAPI server.
```bash
cd backend
python app.py
# or using uvicorn directly:
# uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Navigate to `http://localhost:8000/docs` to see the interactive Swagger UI and test your API!

---

## 🛡️ Model Features

The Machine Learning model actively scores targets based on three vector buckets:
1. **URL & Lexical:** Length anomalies, suspicious IP embeddings, token counts, subdomains, and shortening services.
2. **HTML & Content:** Form hijacking signatures, hidden input counts, script/iframe densities, and external action routing.
3. **Visual Heuristics:** Detection of brand impersonation patterns typically abused in high-profile credential theft campaigns.

---

## 📝 Future Improvements
- Switch to a full headless browser (Playwright) to capture actual rendered DOM screenshots and perform CNN-based Perceptual Image Hashing for the visual similarity pipeline.
- Integrate a caching layer (Redis) to quickly check historically blocked malicious domains before running inference.
- Connect a PostgreSQL database to persistently store logged threats and telemetry data.
