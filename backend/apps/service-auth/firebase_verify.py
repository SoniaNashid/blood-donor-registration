# firebase_verify.py  ← Token validation lives here
# (optionally) users.py, roles.py, auth_utils.py

import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Request, Depends
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    token = auth_header.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        request.state.user = decoded_token
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token verification failed")

        