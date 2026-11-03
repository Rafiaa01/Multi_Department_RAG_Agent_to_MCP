from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from src.config import OPENAI_MODEL
from src.prompt.system_prompt import system_prompt


def create_department_agent(hr_tool, it_tool, finance_tool, calculator_tool):

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0,
    )

    tools = [
        hr_tool,
        it_tool,
        finance_tool,
        calculator_tool,
    ]

    

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    return agent
