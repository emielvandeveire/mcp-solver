from datetime import timedelta
from idp_engine import IDP, model_expand, model_propagate 
from ..core.base_model_manager import BaseModelManager
from .solution import export_solution

class IDPModelManager(BaseModelManager):
    """
    IDP model manager.
    Stores items and executes the selected IDP-Z3 task in solve_model.
    """

    def __init__(self):
        super().__init__()
        self.last_solution = None

    async def solve_model(self, timeout: timedelta, reasoning_task: str = "model_expand") -> dict:
        if not self.code_items:
            result = export_solution(Exception("Model is empty"), reasoning_task)
            self.last_solution = result
            return result

        idp_code = "\n".join(self.code_items)

        try:
            # 1. Parse the code into an IDP model
            kb = IDP.from_str(idp_code)
            
            # 2. Extract the Theory and Structure from the parsed model
            theories = list(kb.theories.values())
            structures = list(kb.structures.values())
            
            if not theories or not structures:
                raise ValueError("The IDP code must contain at least one 'theory' and one 'structure' block.")
                
            T = theories[0]
            S = structures[0]
            
            # 3. Execute the reasoning task and send raw data to export_solution
            if reasoning_task == "model_expand":
                generator = model_expand(T, S, max=1)
                models = list(generator)
                result = export_solution(data=models, reasoning_task=reasoning_task)
                
            elif reasoning_task == "propagate":
                generator = model_propagate(T, S)
                propagated_facts = list(generator)
                result = export_solution(data=propagated_facts, reasoning_task=reasoning_task)
                
            else:
                raise ValueError(f"Reasoning task '{reasoning_task}' is currently not supported.")
            
            self.last_solution = result
            return result

        except Exception as e:
            # Catch system/syntax errors gracefully and pass them through the formatter
            result = export_solution(data=e, reasoning_task=reasoning_task)
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