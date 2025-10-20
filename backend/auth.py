from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import hashlib
from datetime import datetime, timedelta

# Security setup
security = HTTPBearer()

# ============================================================================
# USER DATABASE (Simple - for demo)
# In production, use real database!
# ============================================================================

# Hash passwords for security
def hash_password(password: str) -> str:
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

# Demo users (username: password)
USERS = {
    "demo": hash_password("demo123"),
    "admin": hash_password("admin123"),
    "user": hash_password("password")
}

# Active sessions (token: username)
SESSIONS = {}

# ============================================================================
# MODELS
# ============================================================================

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    message: str
    username: Optional[str] = None

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def create_token() -> str:
    """Generate secure random token"""
    return secrets.token_urlsafe(32)

def authenticate_user(username: str, password: str) -> Optional[str]:
    """
    Authenticate user and return token if successful
    Returns: token if success, None if failed
    """
    hashed_password = hash_password(password)
    
    if username in USERS and USERS[username] == hashed_password:
        # Create session token
        token = create_token()
        SESSIONS[token] = {
            "username": username,
            "created_at": datetime.now()
        }
        return token
    return None

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify token and return username
    Used as dependency in protected routes
    """
    token = credentials.credentials
    
    if token not in SESSIONS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Return username
    return SESSIONS[token]["username"]

def logout_user(token: str) -> bool:
    """Remove token from sessions"""
    if token in SESSIONS:
        del SESSIONS[token]
        return True
    return False

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_active_users() -> int:
    """Get count of active sessions"""
    return len(SESSIONS)

def cleanup_old_sessions(max_age_hours: int = 24):
    """Remove sessions older than max_age_hours"""
    now = datetime.now()
    expired = [
        token for token, data in SESSIONS.items()
        if (now - data["created_at"]).total_seconds() > max_age_hours * 3600
    ]
    for token in expired:
        del SESSIONS[token]