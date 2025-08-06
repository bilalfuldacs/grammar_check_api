"""
Custom exceptions for the Grammar Check API
"""

class GrammarCheckError(Exception):
    """Base exception for grammar checking errors"""
    pass

class OllamaConnectionError(GrammarCheckError):
    """Raised when unable to connect to Ollama"""
    pass

class OllamaTimeoutError(GrammarCheckError):
    """Raised when Ollama request times out"""
    pass

class OllamaResponseError(GrammarCheckError):
    """Raised when Ollama returns an error response"""
    pass

class InvalidResponseError(GrammarCheckError):
    """Raised when unable to parse Ollama response"""
    pass

class ModelNotAvailableError(GrammarCheckError):
    """Raised when the required model is not available"""
    pass

class TextTooLongError(GrammarCheckError):
    """Raised when input text exceeds maximum length"""
    pass

class InvalidInputError(GrammarCheckError):
    """Raised when input text is invalid or empty"""
    pass 