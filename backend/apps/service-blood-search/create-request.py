from fastapi import APIRouter, Query, Depends
from datetime import datetime
from typing import Optional

from database import request_table  # <-- Use this exact name
from service_auth.firebase_verify import verify_token

router = APIRouter()

@router.get("/blood-request")
async def create_blood_search_request(
    blood: str = Query(..., description="Blood type"),
    location: Optional[str] = Query(None, description="City or area"),
    user=Depends(verify_token)
):
    record = {
        "user_id": user["uid"],
        "email": user.get("email", "anonymous"),
        "blood_type": blood,
        "location": location,
        "timestamp": datetime.utcnow()
    }

    await request_table.insert_one(record)

    return {"message": "Request logged successfully."}
