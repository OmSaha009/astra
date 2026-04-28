import json
from core.logging import setup_logger
from .tools.registry import TOOLS

logger = setup_logger(__name__)

class TaskExecutor:
    def __init__(self):
        self.state = {}
        self.steps_log = []

    def execute(self, plan: dict, variables: dict) -> tuple:
        result = None
        for step in plan.get("steps", {}):
            func_name = step["function"]
            args = step.get("args", {}).copy()

            for key, value in args.items():
                if value == "$prev":
                    args[key] = result

                elif isinstance(value, str) and value.startswith("$"):
                    var_name = value[1:]
                    if var_name in self.state:
                        args[key] = self.state[var_name]

            tool = TOOLS.get(func_name)
            if not tool:
                raise ValueError(f"Tool not found: {func_name}")
            
            func =  tool["function"]

            try:
                result = func(**args)
            except Exception as e:  
                logger.error(f"Tool {func_name} failed: {e}")
                raise

            self.state[func_name] = result
            self.state["prev"] = result

            step_desc = f"{func_name}({self._format_args(args)}) -> {result}"
            self.steps_log.append(step_desc)
            logger.debug(f"Step LOGGED: {step_desc}")
        return result, "\n".join(f"Step: {i+1}: {s}" for i,s in enumerate(self.steps_log))
    
    def _format_args(self, args: dict) -> str:
        return ", ".join(f"{k}={v}" for k,v in args.items())
        
