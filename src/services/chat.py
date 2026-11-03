from src.services.session_management import (
    get_or_create_session,
    update_session,
)


def chat_with_history(agent, request):
    history = get_or_create_session(request.session_id)

    history.append({"role": "user", "content": request.message})

    response = agent.invoke(
        {"messages": history},
        config={"recursion_limit": 10},
    )

    # Check which tools the agent selected
    for message in response["messages"]:
        if message.type == "ai" and message.tool_calls:
            for tool_call in message.tool_calls:
                print("Selected tool:", tool_call["name"])
                print("Tool arguments:", tool_call["args"])

    answer = response["messages"][-1].content

    history.append({"role": "assistant", "content": answer})

    # Save updated conversation in JSON
    update_session(request.session_id, history)

    return {"answer": answer, "history": history}
