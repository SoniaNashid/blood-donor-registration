import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "validation_service")

settings = Settings()
