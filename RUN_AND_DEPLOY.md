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

### Deploying the Backend (API & ML Model)

Since this backend contains machine learning packages (Scikit-Learn, Pandas) and API code, it requires a robust cloud platform. **Render**, **Railway**, or **Heroku** are best here. We'll use Render as an example:

1. Push your entire code repository to **GitHub**.
2. Create an account on [Render.com](https://render.com/).
3. Click **New +** and select **Web Service**.
4. Connect your GitHub repository.
5. Setup the deployment:
   - **Root Directory**: `backend`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt` (You might also instruct it to train the model during build by adding `&& python ../data/generate_mock_data.py && python ml/train.py`)
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Click Deploy. Once complete, Render will give you a live URL like `https://phishing-detector-api.onrender.com`.

> Warning: Machine learning deployments require large memory capacities. Scikit-learn models consume significant RAM, so the free tiers on some cloud platforms may crash or boot slowly.

### Deploying the Frontend (React UI)

The frontend is a static bundle of HTML, CSS, and JS. **Vercel** or **Netlify** are perfect for this.

**Preparation**: 
Before deploying, you must tell the frontend where the live deployment of the backend is. Update your API fetch calls in your React code (e.g., `src/components/Scanner.jsx` or similar) from `http://localhost:8000` to your live API URL (e.g., `https://phishing-detector-api.onrender.com`).

**Steps using Vercel**:
1. Go to [Vercel.com](https://vercel.com/) and link your GitHub account.
2. Click **Add New Project** and import your repository.
3. Configure the Build Settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Click **Deploy**. Vercel will build the frontend, and you will receive a lightning-fast live URL for the user interface!

You have successfully built, tested, and deployed an Ensemble-Driven Cyber Threat Intelligence system!
