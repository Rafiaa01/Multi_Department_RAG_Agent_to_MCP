from src.rag.vector_store.store import create_department_vector_store
from src.tools.it_tool import create_it_tool

vector_store = create_department_vector_store("it")

it_tool = create_it_tool(vector_store)

result = it_tool.invoke({
    "query": "What should an employee do if their company laptop stops working?"
})

print(result)