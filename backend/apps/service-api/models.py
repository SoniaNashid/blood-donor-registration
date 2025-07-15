"""
Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime
from bson import ObjectId

### Blood type Enum (optional but recommended) ###
class BloodType(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"

### Donor input model (used for creating new donors) ###
class Donor(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=18, le=65)
    blood_type: BloodType
    location: str

### Donor model for MongoDB ###
class DonorInDB(Donor):
    id: Optional[str] = None  # MongoDB ObjectId as string
    registered_at: Optional[datetime] = None

### Donor response for public-facing API ###
class DonorSearchResponse(BaseModel):
    name: str
    age: int
    blood_type: BloodType
    location: str

### Model for Donor Search Request 
class DonorSearchRequest(BaseModel):
    blood_type: str
    location: Optional[str]
    user_id: str
    email: Optional[str]
    timestamp: datetime
