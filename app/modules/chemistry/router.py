import json
from core.llm_client import get_llm_client
from core.prompts import load_prompt    
from .executor import TaskExecutor
from .tools.registry import TOOLS, get_tools_by_tags
from core.logging import setup_logger

logger = setup_logger(__name__)

class ChemistryRouter:
    def __init__(self):
        self.executor = TaskExecutor()

    def solve(self, question: str) -> dict:
        logger.info(f"Solving question: {question[:50]}")
        client = get_llm_client()
        extract_prompt = load_prompt("prompt_1_chem").replace("[[question]]", question)
        response = client.generate(extract_prompt, stream=False)

        try:
            data = json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse extraction: {response[:200]}")
            return {
                "result": "Could not understand the chemistry problem",
                "explanation": f"Parse error: {e}"
            }
        
        variables = data.get("variables", {})
        tags = data.get("tags", [])
        target = data.get("target", "")
        domain = data.get("domain", "physical_chemistry")


        logger.info(f"Extracted: tags={tags}, variables={variables}, target={target}")
        
        available_tools = get_tools_by_tags(tags)
        tool_names = list(available_tools.keys())

        if not tool_names:
            return {
                "result": "No suitable tools found for this problem",
                "explanation": f"Tags: {tags}\nAvailable tools might not be cover this problem type"
            }
        
        signatures = {}
        for name in tool_names:
            tool = available_tools[name]
            signatures[name] = {
                "args": tool["args"],
                "returns": tool["returns"],
                "description": tool.get("description", "")
            }

        plan_prompt = load_prompt("prompt_2_chem").replace("[[question]]", str(question)).replace("[[variables]]", str(variables)).replace("[[target]]", str(target)).replace("[[tools_list]]", str(json.dumps(tool_names))).replace("[[signatures]]", str(json.dumps(signatures, indent=2)))

        plan_response = client.generate(plan_prompt, stream=False)
        try:
            plan = json.loads(plan_response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse plan: {plan_response[:200]}")
            return {
                "result": "Could not create execution plan.",
                "explanation": f"Plan parse error: {e}"
            }

        logger.info(f"Plan generated: {plan}")

        try:
            result, explanation = self.executor.execute(plan, variables)

        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return {
                "result": "Execution failed.",
                "explanation": f"Error: {e}"
            }
    
        if target:
            final_result = f"{target} = {result}"
        else:
            final_result = str(result)
        
        return {
            "result": final_result,
            "explanation": explanation
        }