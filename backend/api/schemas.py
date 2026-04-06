from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, Optional

class ScanRequest(BaseModel):
    url: str

class FeaturesBreakdown(BaseModel):
    url_based: Dict[str, Any]
    content_based: Dict[str, Any]
    visual_similarity: float

class PredictionResult(BaseModel):
    is_phishing: bool
    phishing_probability: float

class ScanResponse(BaseModel):
    status: str
    url: str
    prediction: PredictionResult
    features_breakdown: Optional[FeaturesBreakdown] = None

class ErrorResponse(BaseModel):
    detail: str
