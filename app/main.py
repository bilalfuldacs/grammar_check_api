from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import GrammarCheckRequest, GrammarCheckResponse, HealthResponse
from .grammar import check_grammar
from .exceptions import (
    GrammarCheckError,
    OllamaConnectionError,
    OllamaTimeoutError,
    OllamaResponseError,
    InvalidResponseError,
    TextTooLongError,
    InvalidInputError
)
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Grammar Check API",
    version="1.0.0",
    description="Simple grammar checking service using Ollama"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags", timeout=5)
            ollama_connected = response.status_code == 200
    except:
        ollama_connected = False
    
    return HealthResponse(
        status="healthy" if ollama_connected else "degraded",
        ollama_connected=ollama_connected
    )

@app.post("/check")
async def grammar_check(request: GrammarCheckRequest):
    try:
        if not request.text or not request.text.strip():
            raise InvalidInputError("Text cannot be empty")
        
        if len(request.text) > 5000:
            raise TextTooLongError("Text too long (max 5000 characters)")
        
        logger.info(f"Checking grammar for text: {request.text[:50]}...")
        
        issues = await check_grammar(request.text)
        
        logger.info(f"Found {len(issues)} grammar issues")
        return GrammarCheckResponse(issues=issues)
        
    except InvalidInputError as e:
        logger.error(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except TextTooLongError as e:
        logger.error(f"Text too long: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except OllamaConnectionError as e:
        logger.error(f"Ollama connection error: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Grammar service unavailable - Ollama not connected. Please ensure Ollama is running."
        )
    except OllamaTimeoutError as e:
        logger.error(f"Ollama timeout error: {e}")
        raise HTTPException(
            status_code=504, 
            detail="Grammar service timeout. The model is taking longer than expected. Please try again."
        )
    except OllamaResponseError as e:
        logger.error(f"Ollama response error: {e}")
        raise HTTPException(status_code=502, detail=f"Ollama service error: {str(e)}")
    except InvalidResponseError as e:
        logger.error(f"Invalid response error: {e}")
        raise HTTPException(status_code=502, detail="Invalid response from grammar service")
    except GrammarCheckError as e:
        logger.error(f"Grammar check error: {e}")
        raise HTTPException(status_code=500, detail=f"Grammar check failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in grammar check: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error. Please check the server logs for more details."
        )

@app.get("/")
async def root():
    return {"message": "Grammar Check API is running!"}
