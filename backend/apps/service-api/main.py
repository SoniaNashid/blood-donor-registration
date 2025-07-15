"""
Functions
(1) Signin
(2) Donor registration
(3) Create Search Request
"""

from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from donor_reg import router as donor_reg_router
from donor_search import router as donor_search_router

load_dotenv()
PORT = int(os.getenv("API_PORT", 8000))

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route
@app.get("/api/test")
def hello():
    return {"message": "Hello from API Service"}

# Include routers
app.include_router(donor_reg_router, prefix="/api")
app.include_router(donor_search_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
