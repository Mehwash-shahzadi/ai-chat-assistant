from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_service import LLMService
from typing import Optional

app = FastAPI(
    title="AI Assistant API",
    description="Backend API for AI Chat Assistant",
    version="1.0.0"
)

# CORS middleware - allows Streamlit to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM service (single instance for all requests)
llm_service = LLMService()

# ============================================================================
# REQUEST/RESPONSE MODELS (Data structures)
# ============================================================================

class QueryRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 150  # Changed default to 150

class QueryResponse(BaseModel):
    response: str
    model: str

class ModelSwitchRequest(BaseModel):
    model_name: str

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def read_root():
    """Root endpoint - check if API is running"""
    return {
        "message": "AI Assistant API is running! 🚀",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "current_model": llm_service.get_current_model()
    }

@app.get("/models")
def get_models():
    """Get list of available AI models"""
    return {
        "models": llm_service.get_available_models(),
        "current": llm_service.get_current_model()
    }

@app.post("/query", response_model=QueryResponse)
def query_llm(request: QueryRequest):
    """Send query to LLM and get response"""
    try:
        print(f"📨 Received query: {request.prompt[:50]}...")
        
        response = llm_service.generate_response(
            request.prompt,
            request.max_tokens
        )
        
        print(f"✅ Generated response from {llm_service.current_model}")
        
        return QueryResponse(
            response=response,
            model=llm_service.current_model
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/switch-model")
def switch_model(request: ModelSwitchRequest):
    """Switch to a different AI model"""
    try:
        result = llm_service.switch_model(request.model_name)
        return {
            "message": result,
            "current_model": llm_service.get_current_model()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

