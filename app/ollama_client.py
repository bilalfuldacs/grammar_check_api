import json
import logging
import httpx
from typing import List, Dict, Any
from .exceptions import (
    OllamaConnectionError, 
    OllamaTimeoutError, 
    OllamaResponseError, 
    InvalidResponseError,
    ModelNotAvailableError,
    GrammarCheckError
)

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
You are a grammar expert. Find grammar errors in this text and return JSON with the exact wrong phrases and their corrections.

Text: {text}

Return JSON like this:
[
  {{
    "wrong": "exact wrong phrase from text",
    "corrected": "corrected version",
    "error_type": "type of error"
  }}
]

Important: Use the exact wrong phrases from the text, not "incorrect text".
"""

async def query_ollama(text: str) -> list[dict]:
    if not text or not text.strip():
        logger.error("Empty or invalid text provided")
        return []
    
    if len(text) > 5000:
        logger.warning(f"Text too long ({len(text)} chars), truncating")
        text = text[:5000]
    
    prompt = PROMPT_TEMPLATE.format(text=text)
    
    payload = {
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        async with httpx.AsyncClient() as client:
            logger.info("Sending request to Ollama...")
            
            response = await client.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code != 200:
                logger.error(f"Ollama request failed: {response.status_code}")
                raise OllamaResponseError(f"Ollama request failed with status {response.status_code}")
            
            data = response.json()
            generated_text = data.get("response", "")
            
            logger.info("Got response from Ollama")
            
            return parse_response(generated_text)
            
    except httpx.ConnectError:
        logger.error("Cannot connect to Ollama. Make sure it's running.")
        raise OllamaConnectionError("Cannot connect to Ollama. Make sure it's running on localhost:11434")
    except httpx.TimeoutException:
        logger.error("Request timed out")
        raise OllamaTimeoutError("Request to Ollama timed out after 120 seconds")
    except OllamaResponseError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise GrammarCheckError(f"Unexpected error during grammar check: {str(e)}")

def parse_response(text: str) -> list[dict]:
    try:
        start = text.find("[")
        end = text.rfind("]")
        
        if start != -1 and end != -1:
            json_str = text[start:end + 1]
            result = json.loads(json_str)
            
            if isinstance(result, list):
                cleaned_results = []
                for item in result:
                    if isinstance(item, dict):
                        cleaned_item = {
                            "wrong": item.get("wrong", ""),
                            "corrected": item.get("corrected", ""),
                            "error_type": item.get("error_type", "unknown")
                        }
                        if cleaned_item["wrong"] and cleaned_item["wrong"] != "incorrect text":
                            cleaned_results.append(cleaned_item)
                
                return cleaned_results
        
        logger.warning("No valid JSON found in response")
        return []
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        raise InvalidResponseError(f"Failed to parse JSON from Ollama response: {str(e)}")
    except Exception as e:
        logger.error(f"Error parsing response: {e}")
        raise InvalidResponseError(f"Error parsing Ollama response: {str(e)}")

async def check_ollama_health() -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json()
                available_models = [model['name'] for model in models.get('models', [])]
                return 'gemma3:1b' in available_models
            return False
    except Exception:
        return False
