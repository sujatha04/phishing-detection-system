from fastapi import APIRouter, HTTPException, Depends
import urllib.parse
import time
import sys
import os

# Ensure backend root is in PYTHONPATH for correct absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schemas import ScanRequest, ScanResponse

# Optional: You could import security dependency to secure this endpoint
# from security import get_current_user_from_token, verify_api_key

try:
    from ml.model import predict
except ImportError:
    print("WARNING: Model files not found. Using a mock prediction function.")
    def predict(features):
        return {"is_phishing": False, "phishing_probability": 0.1}

router = APIRouter()

@router.post("/detect", response_model=ScanResponse)
async def detect_phishing(request: ScanRequest):
    url = request.url
    
    # Ensure scheme
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
        
    try:
        print(f"Analyzing URL: {url}")
        
        # Optional delay (for UI animation)
        time.sleep(1.5)
        
        # ✅ Correct prediction
        result = predict(url)
        
        return ScanResponse(
            status="success",
            url=url,
            prediction=result,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
   
        
