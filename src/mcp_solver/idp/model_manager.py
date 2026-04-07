from datetime import timedelta
from idp_engine import IDP, model_expand 
from ..core.base_model_manager import BaseModelManager

class IDPModelManager(BaseModelManager):
    """
    Simpele IDP model manager voor de MVP.
    Slaat items op en voert IDP-Z3 uit bij solve_model.
    """

    def __init__(self):
        super().__init__()
        self.last_solution = None

    async def solve_model(self, timeout: timedelta, reasoning_task: str = "model_expand") -> dict:
        if not self.code_items:
            return {"satisfiable": False, "status": "error", "error_message": "Model is empty"}

        idp_code = "\n".join(self.code_items)

        try:
            # 1. Parse de code
            kb = IDP.from_str(idp_code)
            
            # 2. Haal de Theory en Structure uit het geparste model
            theories = list(kb.theories.values())
            structures = list(kb.structures.values())
            
            if not theories or not structures:
                raise ValueError("The IDP code must contain at least one 'theory' and one 'structure' block.")
                
            T = theories[0]
            S = structures[0]
            
            # 3. Voer model_expand uit (als LOSSE functie, dus niet kb.model_expand)
            generator = model_expand(T, S, max=1)
            models = list(generator)

            if not models:
                result = {
                    "satisfiable": False,
                    "status": "unsat",
                    "success": True
                }
            else:
                model_str = str(models[0]) 
                result = {
                    "satisfiable": True,
                    "status": "sat",
                    "success": True,
                    "solution": model_str
                }
            
            self.last_solution = result
            return result

        except Exception as e:
            error_msg = str(e)
            result = {
                "satisfiable": False,
                "status": "error",
                "success": True,
                "error_message": f"System or Syntax Error in IDP: {error_msg}"
            }
            self.last_solution = result
            return result

    def get_solution(self) -> dict:
        if not self.last_solution:
            return {"success": False, "message": "No solution available"}
        return {"success": True, "solution": self.last_solution}

    async def clear_model(self) -> dict:
        result = await super().clear_model()
        self.last_solution = None
        result["message"] = "IDP model cleared"
        return result