import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = \"Phishing Detection System API\"
    API_VERSION: str = \"1.0\"
    HOST: str = \"0.0.0.0\"
    PORT: int = 8000
    
    # CORS Settings
    ALLOWED_ORIGINS: list = [\"*\"]
    
    # Model Settings
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR: str = os.path.join(BASE_DIR, 'ml', 'saved_models')
    ENSEMBLE_MODEL_PATH: str = os.path.join(MODEL_DIR, 'ensemble_model.pkl')
    FEATURE_COLS_PATH: str = os.path.join(MODEL_DIR, 'feature_cols.pkl')
    
    # Phishing Threshold (Probability > threshold -> Phishing)
    PHISHING_THRESHOLD: float = 0.5
    
    # Feature Extraction Settings
    REQUEST_TIMEOUT: int = 5
    USER_AGENT: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    class Config:
        case_sensitive = True

# Instantiate global settings
settings = Settings()
