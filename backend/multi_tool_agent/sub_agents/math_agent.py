import re
from google.adk.agents import Agent


    
ARITH_EXPR_RE = re.compile(r'^\s*([-+]?\d+(\.\d+)?)(\s*[-+*/]\s*([-+]?\d+(\.\d+)?))*\s*$')

def is_valid_expression(expr: str) -> bool:
        """
        Check if the expression is a valid basic arithmetic expression.
        Supports +, -, *, / with integers or floats.
        """
        return bool(ARITH_EXPR_RE.match(expr))

def calculate(expr: str) -> float:
        """
        Evaluate a basic arithmetic expression after validation.
        Raises ValueError if the expression is invalid.
        """
        if not is_valid_expression(expr):
            raise ValueError("Invalid arithmetic expression")
        # Safe eval: only allow arithmetic operators and numbers
        allowed_chars = re.compile(r'^[\d\s\.\+\-\*/]+$')
        if not allowed_chars.match(expr):
            raise ValueError("Expression contains invalid characters")
        try:
            return eval(expr, {"__builtins__": None}, {})
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")

mathsAgent = Agent(
        name="MathsAgent",
        description="Handles basic arithmetic calculations using the calculate tool.",
        instruction=("You are a math agent. You ONLY task is to perform basic mathematical arithematic calculations."
        "Use the calculate tool to perform the calculations."
        "Do not engage in any other conversation or tasks."),

        model="gemini-2.0-flash",
        tools=[calculate],
    )