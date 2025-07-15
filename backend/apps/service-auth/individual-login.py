from fastapi import APIRouter, HTTPException
from models import Donor
from database import donors_collection
from datetime import datetime
from bson import ObjectId

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from service_auth.firebase_verify import verify_token

router = APIRouter()

from models import DonorInDB

def donor_helper(donor) -> DonorInDB:
    return DonorInDB(
        id=str(donor["_id"]),
        name=donor["name"],
        age=donor["age"],
        blood_type=donor["blood_type"],
        location=donor["location"],
        registered_at=donor.get("registered_at")
    )

@router.post("/donor-registration", status_code=201)
async def donor_registration(donor: Donor):
    existing = await donors_collection.find_one({
        "name": donor.name,
        "blood_type": donor.blood_type
    })

    if existing:
        raise HTTPException(status_code=409, detail="Donor already exists.")

    donor_data = donor.dict()
    donor_data["registered_at"] = datetime.utcnow()

    result = await donors_collection.insert_one(donor_data)
    new_donor = await donors_collection.find_one({"_id": result.inserted_id})

    return {
        "message": f"Donor {donor.name} registered successfully.",
        "donor": donor_helper(new_donor)
    }
