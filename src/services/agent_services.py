from src.agent.tools_agent import create_department_agent
from src.rag.vector_store.store import create_all_vector_stores
from src.tools.finance_tool import create_finance_tool
from src.tools.hr_tool import create_hr_tool
from src.tools.it_tool import create_it_tool
from src.tools.safe_calculator_tool import calculator_tool


def initialize_agent():

    # Create department vector stores
    vector_stores = create_all_vector_stores()

    # Create department search tools
    hr_tool = create_hr_tool(vector_stores["hr"])
    it_tool = create_it_tool(vector_stores["it"])
    finance_tool = create_finance_tool(vector_stores["finance"])

    # Create the agent with all tools
    agent = create_department_agent(
        hr_tool,
        it_tool,
        finance_tool,
        calculator_tool,
    )

    return agent
