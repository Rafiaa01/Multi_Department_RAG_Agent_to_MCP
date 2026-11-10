
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.config import OPENAI_MODEL
from src.prompt.system_prompt import system_prompt


def create_department_agent(tools):

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0,
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    return agent
