import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your router
from api.routes import router as api_router

# Create FastAPI app
app = FastAPI(
    title="Phishing Detection System API",
    version="1.0"
)

# ✅ FIXED CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # React frontend
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routes
app.include_router(api_router, prefix="/api")

# Run server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)