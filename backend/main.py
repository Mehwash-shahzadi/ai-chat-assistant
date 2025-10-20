from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_service import LLMService
from auth import (
    LoginRequest, 
    LoginResponse, 
    authenticate_user, 
    verify_token, 
    logout_user,
    get_active_users
)
from typing import Optional

app = FastAPI(
    title="AI Assistant API",
    description="Backend API with Authentication",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM service
llm_service = LLMService()

# ============================================================================
# MODELS
# ============================================================================

class QueryRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 150

class QueryResponse(BaseModel):
    response: str
    model: str

class ModelSwitchRequest(BaseModel):
    model_name: str

# ============================================================================
# PUBLIC ENDPOINTS (No auth required)
# ============================================================================

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "AI Assistant API with Authentication 🔐",
        "status": "active",
        "version": "1.0.0",
        "active_users": get_active_users()
    }

@app.get("/health")
def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "current_model": llm_service.get_current_model(),
        "active_users": get_active_users()
    }

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """
    Login endpoint - returns token if successful
    
    Demo accounts:
    - username: demo, password: demo123
    - username: admin, password: admin123
    """
    print(f"🔐 Login attempt: {request.username}")
    
    token = authenticate_user(request.username, request.password)
    
    if token:
        print(f"✅ Login successful: {request.username}")
        return LoginResponse(
            success=True,
            token=token,
            message="Login successful!",
            username=request.username
        )
    else:
        print(f"❌ Login failed: {request.username}")
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

@app.post("/logout")
def logout(token: str):
    """Logout endpoint"""
    success = logout_user(token)
    return {
        "success": success,
        "message": "Logged out successfully" if success else "Invalid token"
    }

# ============================================================================
# PROTECTED ENDPOINTS (Auth required)
# ============================================================================

@app.get("/models")
def get_models(username: str = Depends(verify_token)):
    """Get available models - PROTECTED"""
    print(f"📋 {username} requested models")
    return {
        "models": llm_service.get_available_models(),
        "current": llm_service.get_current_model()
    }

@app.post("/query", response_model=QueryResponse)
def query_llm(request: QueryRequest, username: str = Depends(verify_token)):
    """Send query to LLM - PROTECTED"""
    try:
        print(f"📨 {username} sent query: {request.prompt[:50]}...")
        
        response = llm_service.generate_response(
            request.prompt,
            request.max_tokens
        )
        
        print(f"✅ Response generated for {username}")
        
        return QueryResponse(
            response=response,
            model=llm_service.current_model
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/switch-model")
def switch_model(request: ModelSwitchRequest, username: str = Depends(verify_token)):
    """Switch AI model - PROTECTED"""
    print(f"🔄 {username} switching to {request.model_name}")
    result = llm_service.switch_model(request.model_name)
    return {
        "message": result,
        "current_model": llm_service.get_current_model()
    }
