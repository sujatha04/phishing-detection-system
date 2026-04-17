# Complete Guide: Running and Deploying the Phishing Detection System

This guide walks you through the entire process of setting up, running locally, and deploying both the backend (FastAPI + Machine Learning) and the frontend (React + Vite) application.

## Part 1: Running the Application Locally (Step-by-Step)

### Step 1: Initialize the Backend
You will need to install the necessary Python libraries that will power the FastAPI server, the web extractors, and the machine learning model.

1. Open your terminal in the root directory `phishing-detection-system/`
2. Change into the backend directory:
   ```bash
   cd backend
   ```
3. *(Optional but recommended)* Create a virtual environment to keep your dependencies isolated:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
4. Install all the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Initialize Machine Learning Model
The backend needs a trained ensemble model to make predictions. We have a robust mock dataset generating script ready to simulate a production-grade ML scenario.

1. If you are not in the root directory, navigate there:
   ```bash
   cd ..
   ```
2. Generate the mock training dataset:
   ```bash
   python data/generate_mock_data.py
   ```
   *(This will create `data/phishing_dataset.csv`)*
3. Train the backend model:
   ```bash
   python backend/ml/train.py
   ```
   *(This will serialize the intelligence models into `backend/ml/saved_models/`)*

### Step 3: Start the Backend Server
Now that the API endpoint and the model are ready, let's turn the server on.

1. Ensure you are in the `backend/` folder:
   ```bash
   cd backend
   ```
2. Start the Uvicorn ASGI server:
   ```bash
   python app.py
   ```
3. Your API will be listening on `http://localhost:8000`. 
   > Note: You can navigate to `http://localhost:8000/docs` to test endpoints and read automatic Swagger documentation!

### Step 4: Run the Frontend Application
Leave the backend terminal running. Open a **new terminal tab** to start the React interface.

1. In the new terminal, change into your frontend directory:
   ```bash
   cd frontend
   ```
2. Install the JavaScript package dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. The terminal will give you a local URL (typically `http://localhost:5173`). Click it or paste it into your browser and you can start scanning URLs!

---

## Part 2: Deployment Guide

When you are ready to publish the system on the internet to show clients or reviewers, you will deploy the Backend and Frontend separately.

### 🚀 Deploying the Backend to Render

Now that we've optimized the backend, deployment is straightforward.

1.  **Commit and Push**: Ensure all changes (including the new `Procfile` and cleaned `requirements.txt`) are pushed to your GitHub repository.
2.  **Create Render Web Service**:
    *   Log in to [Render.com](https://render.com/).
    *   Click **New +** > **Web Service**.
    *   Connect your GitHub repository.
3.  **Configure Settings**:
    *   **Name**: `phishing-detection-api` (or your choice).
    *   **Root Directory**: `backend`
    *   **Environment**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4.  **Wait for Build**: Render will automatically install the lean dependencies and start the server.
5.  **Update Frontend**: Once the backend is live, copy the URL (e.g., `https://your-app.onrender.com`) and update your frontend's API URL.

---

### 🛠️ Troubleshooting & Tips

*   **Memory Errors**: If the build fails with "Out of Memory", it's usually because of `pandas` or `scikit-learn`. Our new `requirements.txt` minimizes this risk.
*   **ModuleNotFoundError**: If this occurs, ensure the **Root Directory** in Render is set to `backend`.
*   **CORS Issues**: The `app.py` is already configured to allow all origins (`*`) for easy deployment.

You have successfully optimized and prepared your system for production!
