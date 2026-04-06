import os
import joblib
from core.whitelist import is_whitelisted

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'saved_models')

_model = None
_vectorizer = None

def load_model():
    global _model, _vectorizer
    
    model_path = os.path.join(MODEL_DIR, 'ensemble_model.pkl')
    vectorizer_path = os.path.join(MODEL_DIR, 'vectorizer.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        raise FileNotFoundError("Model or vectorizer not found. Run train.py first.")
        
    _model = joblib.load(model_path)
    _vectorizer = joblib.load(vectorizer_path)

def predict(url: str) -> dict:
    """
    Takes a URL string and returns prediction using TF-IDF model.
    """
    if _model is None or _vectorizer is None:
        load_model()
    
    # 🚨 CHECK WHITELIST FIRST (Safety override)
    if is_whitelisted(url):
        return {
            "is_phishing": False,
            "phishing_probability": 0.0,
            "confidence": 1.0,
            "is_whitelisted": True,
            "message": "This is a verified legitimate domain."
        }
    
    # ✅ Convert URL → vector
    X = _vectorizer.transform([url])
    
    # Predict probability
    prob = float(_model.predict_proba(X)[0][1])
    
    is_phishing = prob > 0.5
    
    return {
        "is_phishing": is_phishing,
        "phishing_probability": prob,
        "confidence": prob if is_phishing else (1 - prob)
    }