"""
Authentication & Authorization API Route Controller
Author: Ravi Ranjan Singh
"""

import time
import uuid
from src.backend.core.security import hash_password, verify_password, create_access_token
from src.backend.core.database import db

def handle_register(payload: dict) -> tuple:
    email = payload.get("email", "").lower().strip()
    password = payload.get("password", "")
    full_name = payload.get("full_name", "")
    
    if not email or not password or len(password) < 6:
        return {"status": "error", "message": "Valid email and password (min 6 chars) required."}, 400
        
    if email in db.users:
        return {"status": "error", "message": "User with this email already exists."}, 400
        
    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    user_record = {
        "user_id": user_id,
        "email": email,
        "password_hash": hash_password(password),
        "full_name": full_name,
        "age": payload.get("age", 25),
        "gender": payload.get("gender", "male"),
        "height_cm": payload.get("height_cm", 175.0),
        "weight_kg": payload.get("weight_kg", 70.0),
        "created_at": time.time()
    }
    
    db.users[email] = user_record
    
    return {
        "status": "success",
        "message": "User registered successfully.",
        "data": {
            "user_id": user_id,
            "email": email,
            "full_name": full_name
        }
    }, 201

def handle_login(payload: dict) -> tuple:
    email = payload.get("email", "").lower().strip()
    password = payload.get("password", "")
    
    user = db.users.get(email)
    if not user or not verify_password(password, user["password_hash"]):
        return {"status": "error", "message": "Invalid email or password credentials."}, 401
        
    access_token = create_access_token({"sub": user["user_id"], "email": email})
    
    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 900
    }, 200
