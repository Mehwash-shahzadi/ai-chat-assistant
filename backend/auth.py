from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import bcrypt
from datetime import datetime, timedelta

# Security setup
security = HTTPBearer()
# ====================================================================
# SESSION-BASED AUTHENTICATION SYSTEM (STATEFUL)
# ====================================================================
# This authentication system uses server-side sessions.
# When a user logs in:
#   1. The server creates a random token (like a session ID).
#   2. The token is stored in the SESSIONS dictionary with user info.
#   3. The token is returned to the client.
#   4. The client must send this token with every request.
# The server validates tokens by checking them in the SESSIONS dict.
# If the token exists, the user is authenticated.
# If not, the session has expired or the user is logged out.
# =====================================================================


# ======================================================================
# USER DATABASE (Professional with Bcrypt)
# =======================================================================

def hash_password(password: str) -> str:
    """Hash password using bcrypt - Industry standard!"""
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hashed version"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

# Pre-hashed passwords for demo users
# To add new user: print(hash_password("your_password"))
USERS = {
    "demo": hash_password("demo123"),
    "admin": hash_password("admin123"),
    "user": hash_password("password"),
    # Add more users here
}


# Active sessions (token: user_data)
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

class UserInfo(BaseModel):
    username: str
    login_time: str
    session_duration: str

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def create_token() -> str:
    """Generate cryptographically secure random token"""
    return secrets.token_urlsafe(32)

def authenticate_user(username: str, password: str) -> Optional[str]:
    """
    Authenticate user with bcrypt password verification
    Returns: token if success, None if failed
    """
    # Check if user exists
    if username not in USERS:
        # Prevent timing attacks by still checking password
        bcrypt.checkpw(b"dummy", bcrypt.gensalt())
        return None
    
    # Verify password using bcrypt
    if verify_password(password, USERS[username]):
        # Create secure session token
        token = create_token()
        SESSIONS[token] = {
            "username": username,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        print(f"✅ Authentication successful: {username}")
        return token
    
    print(f"❌ Authentication failed: {username}")
    return None

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify JWT-like token and return username
    Used as dependency in protected routes
    """
    token = credentials.credentials
    
    if token not in SESSIONS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please login again."
        )
    
    # Update last activity
    SESSIONS[token]["last_activity"] = datetime.now()
    
    # Check if session is too old (24 hours)
    session_age = datetime.now() - SESSIONS[token]["created_at"]
    if session_age > timedelta(hours=24):
        del SESSIONS[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please login again."
        )
    
    return SESSIONS[token]["username"]

def logout_user(token: str) -> bool:
    """Remove token from active sessions"""
    if token in SESSIONS:
        username = SESSIONS[token]["username"]
        del SESSIONS[token]
        print(f"🚪 User logged out: {username}")
        return True
    return False

def get_user_info(token: str) -> Optional[UserInfo]:
    """Get user session information"""
    if token not in SESSIONS:
        return None
    
    session = SESSIONS[token]
    created = session["created_at"]
    duration = datetime.now() - created
    
    return UserInfo(
        username=session["username"],
        login_time=created.strftime("%Y-%m-%d %H:%M:%S"),
        session_duration=str(duration).split('.')[0]  # Remove microseconds
    )

# ============================================================================
# ADMIN FUNCTIONS
# ============================================================================

def get_active_users() -> int:
    """Get count of active sessions"""
    return len(SESSIONS)

def get_all_sessions() -> list:
    """Get all active sessions (admin only)"""
    return [
        {
            "username": data["username"],
            "login_time": data["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
            "last_activity": data["last_activity"].strftime("%H:%M:%S")
        }
        for token, data in SESSIONS.items()
    ]

def cleanup_old_sessions(max_age_hours: int = 24):
    """Remove sessions older than max_age_hours"""
    now = datetime.now()
    expired = [
        token for token, data in SESSIONS.items()
        if (now - data["created_at"]).total_seconds() > max_age_hours * 3600
    ]
    for token in expired:
        username = SESSIONS[token]["username"]
        del SESSIONS[token]
        print(f"🧹 Cleaned up expired session: {username}")
    
    return len(expired)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def add_user(username: str, password: str) -> bool:
    """
    Add new user to database
    Usage: add_user("newuser", "securepassword")
    """
    if username in USERS:
        return False
    
    USERS[username] = hash_password(password)
    print(f"➕ New user added: {username}")
    return True

def change_password(username: str, old_password: str, new_password: str) -> bool:
    """Change user password"""
    if username not in USERS:
        return False
    
    if not verify_password(old_password, USERS[username]):
        return False
    
    USERS[username] = hash_password(new_password)
    print(f"🔄 Password changed for: {username}")
    return True

# ============================================================================
# FOR TESTING - Generate hashed passwords
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 PASSWORD HASH GENERATOR")
    print("=" * 60)
    
    test_passwords = {
        "demo123": hash_password("demo123"),
        "admin123": hash_password("admin123"),
        "password": hash_password("password")
    }
    
    print("\n📝 Hashed passwords:")
    for pwd, hashed in test_passwords.items():
        print(f"\nPassword: {pwd}")
        print(f"Hash: {hashed}")
        print(f"Verify: {verify_password(pwd, hashed)}")
    
    print("\n" + "=" * 60)
    print("✅ Bcrypt authentication is working!")
    print("=" * 60)