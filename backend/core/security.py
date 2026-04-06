import os
from datetime import datetime, timedelta
from typing import Optional, Union, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from passlib.context import CryptContext
import jwt

# Since config is in the same directory, import it here
try:
    from backend.config import settings
except ImportError:
    # If starting from backend dir directly
    from config import settings

# --- Password Hashing Setup ---
# Using passlib with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- JWT Setup ---
# Consider adding these to config.py later
SECRET_KEY = os.environ.get("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- API Key Setup (Alternative to JWT) ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Optional static API key for simple service-to-service auth
# Consider setting this in environment variables or config
STATIC_API_KEY = os.environ.get("STATIC_API_KEY", "your-static-phishing-api-key-here")


# --- Functions ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a password."""
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Creates a JSON Web Token (JWT)."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verifies a JWT token and returns the subject (usually user ID)."""
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data.get("sub")
    except jwt.PyJWTError:
        return None

async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    """FastAPI Dependency for JWT token validation."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = verify_token(token)
    if user_id is None:
        raise credentials_exception
    
    # Normally you would fetch the user from database here using user_id
    # user = db.get_user(user_id)
    # if user is None:
    #     raise credentials_exception
    # return user
    return user_id

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """FastAPI Dependency for static API key validation."""
    if api_key == STATIC_API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Could not validate API KEY"
    )
