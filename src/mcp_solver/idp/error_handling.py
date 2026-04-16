"""
IDP-Z3 error handling module.

This module provides enhanced error handling for IDP operations, including:
- Function wrappers that capture and translate IDP-Z3 exceptions
- Structured error reporting for better user experience for the LLM
"""

import functools
import logging
import traceback
from collections.abc import Callable
from typing import Any, TypeVar

logger = logging.getLogger(__name__)
T = TypeVar("T")

# Map of common IDP-Z3 exceptions to user-friendly messages
EXCEPTION_MESSAGES = {
    # Parser Errors (Syntactic)
    "UnexpectedToken": "Syntax error: unexpected token. Check for missing '.' at the end of sentences, or missing brackets '{}'.",
    "UnexpectedCharacters": "Syntax error: unexpected character. Check your spelling and ensure you use valid IDP-Z3 symbols.",
    
    # IDP-Z3 Logic Errors (Semantic)
    "IDPZ3Error": "Logic or Type error: The theory is syntactically correct, but there is a problem with your types or definitions.",
    "TypeError": "Type error: variable or predicate types do not match your vocabulary.",
    
    # Solver/System Errors
    "ValueError": "Value error: The input is valid IDP, but the requested operation (like a specific reasoning task) failed.",
    "AttributeError": "Operation error: You are trying to use a feature that is not available or incorrectly called.",
}

class IDPError(Exception):
    """Custom exception class for enhanced IDP errors."""

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
        context: str | None = None,
    ):
        self.original_error = original_error
        self.original_traceback = traceback.format_exc()
        enhanced_message = message
        
        if context:
            enhanced_message += f"\nHere are more error details:\n{context}"
            
        # Include the original error message, but keep it concise to avoid overwhelming the LLM with tokens
        if original_error:
            error_type = type(original_error).__name__
            # Take only the first 500 characters of the original error to avoid token bloat
            error_msg = str(original_error)[:500] + ("..." if len(str(original_error)) > 500 else "")
            enhanced_message += f"\n\nOriginal error ({error_type}): {error_msg}"
            
        super().__init__(enhanced_message)


def format_solution_error(error: Exception) -> dict[str, Any]:
    error_type = type(error).__name__
    error_msg = str(error)
    
    friendly_message = EXCEPTION_MESSAGES.get(error_type)
    if not friendly_message:
        for pattern, message in EXCEPTION_MESSAGES.items():
            if pattern in error_msg or pattern in error_type:
                friendly_message = message
                break
                
    friendly_message = friendly_message or "An error occurred while evaluating the IDP-Z3 model."
    short_original = error_msg[:250] + ("..." if len(error_msg) > 250 else "")
    final_message = f"{friendly_message}\n\nTechnical details:\n{short_original}"
    
    logger.error(f"Handled IDP error ({error_type}): {final_message}")

    return {
        "satisfiable": False,
        "status": "error",
        "success": True, # True is required by MCP, otherwise the server breaks
        "error_type": error_type,
        "error_message": final_message,
    }