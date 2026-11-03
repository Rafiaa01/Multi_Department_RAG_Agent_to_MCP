import ast
import operator

from langchain.tools import tool

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str):

    if len(expression) > 100:
        raise ValueError("Expression is too long")

    def evaluate(node):

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large")

            return OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))

        raise ValueError("Unsupported mathematical expression")

    tree = ast.parse(expression, mode="eval")
    result = evaluate(tree.body)

    if abs(result) > 1_000_000_000_000:
        raise ValueError("Result is too large")

    return result


@tool
def calculator_tool(expression: str) -> str:
    """Perform basic arithmetic calculations using numbers and operators such as +, -, *, /, %, and **."""

    try:
        result = calculate(expression)
        return str(result)

    except Exception as e:  # noqa: BLE001
        return f"Calculation error: {str(e)}"  # noqa: RUF010
