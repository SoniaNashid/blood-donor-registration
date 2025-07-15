from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from app.validators.search_validator import validate_search_request
from app.database import request_table, donor_search_ready
from datetime import datetime

app = FastAPI()

from fastapi import Query
from typing import Optional
from datetime import datetime

@app.get("/validate/dashboard")
async def dashboard(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    blood_type: Optional[str] = Query(None, description="Filter by blood type"),
    start_date: Optional[str] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter by end date (YYYY-MM-DD)")
):
    query = {}

    if user_id:
        query["user_id"] = user_id

    if blood_type:
        query["blood_type"] = blood_type

    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["$gte"] = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            date_filter["$lte"] = datetime.strptime(end_date, "%Y-%m-%d")
        query["timestamp"] = date_filter

    cursor = request_table.find(query).sort("timestamp", -1)
    records = []
    async for doc in cursor:
        records.append({
            "request_id": str(doc["_id"]),
            "user_id": doc["user_id"],
            "blood_type": doc["blood_type"],
            "location": doc.get("location", ""),
            "timestamp": doc.get("timestamp")
        })

    return records


@app.post("/validate/process")
async def process_request(form: ProcessForm):
    request_id = form.request_id

    # Ensure request exists
    search_req = await request_table.find_one({"_id": ObjectId(request_id)})
    if not search_req:
        raise HTTPException(status_code=404, detail="Search request not found.")

    # Save processed entry
    result = {
        "request_id": ObjectId(request_id),
        "status": form.status,
        "comment": form.comment,
        "processed_at": datetime.utcnow()
    }
    await donor_search_ready.insert_one(result)

    return {"message": "Search request processed successfully."}
