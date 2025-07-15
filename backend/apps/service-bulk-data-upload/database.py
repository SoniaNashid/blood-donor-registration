"""
MongoDB client setup
"""

"""Put this in env file
MONGO_URI=mongodb://localhost:27017
MONGO_DB=blood_donor_app
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "blood_donor_app")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

donors_collection = db["donors"]
request_collection = db["request_table"]
