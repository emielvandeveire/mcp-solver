"""
IDP solution module for extracting and formatting solutions from IDP solvers.

This module provides functions for extracting solution data from IDP solvers
and converting it to a standardized format.
"""
import logging
import re
from typing import Any
from .error_handling import format_solution_error

# Matches "term := value." lines emitted in IDP-Z3 model output.
_ASSIGNMENT_RE = re.compile(r"^\s*(.+?)\s*:=\s*(.+?)\s*\.?\s*$")

logger = logging.getLogger(__name__)

_LAST_SOLUTION = None


def format_explanation_output(facts, laws) -> dict[str, Any]:
    """
    # Format the (facts, laws) tuple returned by explain into a structured dict
    """
    fact_strs = [str(f) for f in (facts or [])]
    law_strs = [str(l) for l in (laws or [])]

    return {
        "conflicting_facts": fact_strs,
        "conflicting_laws": law_strs,
        "hint": "The facts above (from the structure) together with the laws above (from the theory) are jointly unsatisfiable. Resolve the conflict by relaxing one of the facts or weakening one of the laws.",
    }

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
            error_solution = format_solution_error(data)
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
                
        elif reasoning_task == "satisfiability":
            is_sat = bool(data) # true if we have any models
            solution_data = {
                "satisfiable": is_sat,
                "status": "sat" if is_sat else "unsat",
                "solution": {"result": "The theory is satisfiable." if is_sat else "The theory is unsatisfiable."}
            }

        elif reasoning_task == "optimize":
            if not data:
                solution_data = {
                    "satisfiable": False, 
                    "status": "unsat", 
                    "error_message": "No models found to optimize. The theory might be unsatisfiable."
                }
            else:
                solution_data = {
                    "satisfiable": True, 
                    "status": "optimal", 
                    "solution": {"model_output": str(data[0])}
                }
        
        elif reasoning_task == "explain":
            if isinstance(data, tuple) and len(data) == 2:
                facts, laws = data
                solution_data = {
                    "satisfiable": False,
                    "status": "unsat_explained",
                    "solution": format_explanation_output(facts, laws)
                }
            else:
                solution_data = {
                    "satisfiable": False,
                    "status": "error",
                    "error_message": f"Expected a tuple of (facts, laws) for the 'explain' task, but got {type(data)}."
                }

        elif reasoning_task == "determine_range":
            if not data:
                solution_data = {
                    "satisfiable": False,
                    "status": "unsat",
                    "error_message": "No models found; cannot determine ranges."
                }
            else:
                ranges: dict[str, set[str]] = {}
                for model in data:
                    for line in str(model).splitlines():
                        m = _ASSIGNMENT_RE.match(line)
                        if not m:
                            continue
                        term, value = m.group(1).strip(), m.group(2).strip()
                        if not term or not value:
                            continue
                        ranges.setdefault(term, set()).add(value)

                ranges_out = {term: sorted(values) for term, values in ranges.items()}
                solution_data = {
                    "satisfiable": True,
                    "status": "range_determined",
                    "model_count": len(data),
                    "solution": ranges_out,
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