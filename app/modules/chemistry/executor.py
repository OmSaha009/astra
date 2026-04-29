import json
from core.logging import setup_logger
from .tools.registry import TOOLS

logger = setup_logger(__name__)

import inspect

ARG_ALIASES = {
                    "volume_L": "volume",
                    "volume_ml": "volume",
                    "mass": "mass",
                    "molar_mass": "molar_mass",
                    "moles": "moles",
                    "M": "molarity",
                    "m": "molality",
                    "wv_percent": "wv_percent",
                    # Add as you find mismatches
                }

def safe_call(func, args):
    """Call function with only the arguments it expects"""
    sig = inspect.signature(func)
    expected_args = set(sig.parameters.keys())
    
    # First map aliases, then filter
    mapped = {}
    for key, value in args.items():
        new_key = ARG_ALIASES.get(key, key)
        if new_key in expected_args:
            mapped[new_key] = value
        else:
            print(f"DEBUG: Skipping unexpected argument: {key} -> {new_key}")
    
    # Check for missing required args
    missing = expected_args - set(mapped.keys())
    if missing:
        raise ValueError(f"Missing required arguments: {missing}")
    
    return func(**mapped)

def resolve_value(value, prev_result):
    """Resolve $prev and evaluate simple arithmetic expressions"""
    if isinstance(value, str) and "$prev" in value:
        # Replace $prev with the actual numeric result
        expr = value.replace("$prev", str(prev_result))
        try:
            # Evaluate the arithmetic expression
            return eval(expr)
        except:
            return expr
    return value

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
                resolved_args = {}
                for key, val in args.items():
                    resolved_args[key] = resolve_value(val, result)  # result is previous step's output

                result = safe_call(func, resolved_args)

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
        
