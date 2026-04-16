"""
IDP solution module for extracting and formatting solutions from IDP solvers.

This module provides functions for extracting solution data from IDP solvers
and converting it to a standardized format.
"""
import logging
from typing import Any

logger = logging.getLogger(__name__)

_LAST_SOLUTION = None

def export_solution(
    data: Any = None,
    reasoning_task: str = "model_expand",
    status: str | None = None,
) -> dict[str, Any]:
    """
    Extract and format solutions from IDP-Z3 based on the reasoning task.
    """
    global _LAST_SOLUTION

    try:
        # If we receive an Exception, format it directly as an error
        if isinstance(data, Exception):
            error_solution = {
                "satisfiable": False,
                "status": "error",
                "success": True,  # True is required by MCP, otherwise the server breaks
                "error_message": f"IDP Error: {str(data)}"
            }
            _LAST_SOLUTION = error_solution
            return error_solution

        solution_data = {}

        # Format the solution differently based on the reasoning task, since the data structure can differ significantly
        if reasoning_task == "model_expand":
            # data is a list of models here
            if not data:
                solution_data = {
                    "satisfiable": False, 
                    "status": "unsat", 
                    "solution": {"result": "No models found"} # Wrapped in dict
                }
            else:
                solution_data = {
                    "satisfiable": True, 
                    "status": "sat", 
                    "solution": {"model_output": str(data[0])} # Wrapped in dict
                }

        elif reasoning_task == "propagate":
            # data is the list of derived facts here
            prop_strings = [str(item) for item in data]
            # Check if IDP-Z3 found a contradiction during propagation
            if any("Not satisfiable" in s for s in prop_strings):
                solution_data = {
                    "satisfiable": False, 
                    "status": "unsat", 
                    "error_message": "Theory is unsatisfiable (contradiction found during propagation). Check your exceptions and default rules."
                }
            else:
                # Build a dictionary mapping facts to True/False 
                solution_dict = {}
                for s in prop_strings:
                    if s == "No more consequences.":
                        continue
                    if s.startswith("Not "):
                        solution_dict[s[4:]] = False # Ex: "Not flies(Opus)" -> {"flies(Opus)": False}
                    else:
                        solution_dict[s] = True # Ex: "flies(Tweety)" -> {"flies(Tweety)": True}
                
                solution_data = {
                    "satisfiable": True, 
                    "status": "propagated", 
                    "solution": solution_dict
                }
            
        else:
            # Fallback for tasks that are not yet implemented (such as explain, optimize)
            solution_data = {
                "satisfiable": False, 
                "status": "error", 
                "error_message": f"Unsupported reasoning task: {reasoning_task}"
            }

        # Success-flag requied for safe handling by the server
        solution_data["success"] = True
        
        _LAST_SOLUTION = solution_data
        return solution_data

    except Exception as e:
        error_solution = {
            "satisfiable": False,
            "status": "error",
            "success": True,
            "error_message": f"Error formatting IDP solution: {str(e)}"
        }
        _LAST_SOLUTION = error_solution
        logger.error(f"Error in IDP export_solution: {e!s}", exc_info=True)
        return error_solution