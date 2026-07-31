"""
Security, Password Hashing & JWT Token Management
Author: Ravi Ranjan Singh
"""

import hmac
import hashlib
import base64
import json
import time
from typing import Dict, Any, Optional
from src.backend.core.config import settings

def hash_password(password: str) -> str:
    """Hashes password using HMAC-SHA256 with salt."""
    salt = settings.SECRET_KEY.encode("utf-8")
    pwd_bytes = password.encode("utf-8")
    hashed = hmac.new(salt, pwd_bytes, hashlib.sha256).hexdigest()
    return f"sha256${hashed}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plaintext password against hashed digest using constant-time comparison (CWE-208 mitigation)."""
    computed_hash = hash_password(plain_password)
    return hmac.compare_digest(computed_hash.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    now = int(time.time())
    expire = now + (expires_delta or (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60))
    to_encode.update({"iat": now, "exp": expire})
    
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode("utf-8")).decode("utf-8").rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(to_encode).encode("utf-8")).decode("utf-8").rstrip("=")
    
    signature_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(settings.SECRET_KEY.encode("utf-8"), signature_input, hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and validates JWT token with constant-time signature comparison."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
            
        header_b64, payload_b64, signature_b64 = parts
        
        # Verify Signature
        signature_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        expected_sig = hmac.new(settings.SECRET_KEY.encode("utf-8"), signature_input, hashlib.sha256).digest()
        expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode("utf-8").rstrip("=")
        
        if not hmac.compare_digest(signature_b64.encode("utf-8"), expected_sig_b64.encode("utf-8")):
            return None
            
        # Base64 decode payload
        rem = len(payload_b64) % 4
        if rem > 0:
            payload_b64 += "=" * (4 - rem)
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))
        
        # Check Expiration
        if payload.get("exp") and int(time.time()) > payload["exp"]:
            return None
            
        return payload
    except Exception:
        return None
