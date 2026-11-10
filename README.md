# Multi-Department RAG Agent with MCP

An intelligent internal knowledge assistant built using **Python, FastAPI, LangChain, FastMCP, and LLM-powered agents**.

The application answers employee questions using HR, IT Support, and Finance policy documents. It uses an agentic RAG architecture with independent MCP servers, allowing the AI agent to dynamically discover and execute department-specific tools.

## Features

- **Multi-Department RAG:** Separate retrieval functionality for HR, IT, and Finance.
- **MCP Integration:** Three independent FastMCP servers using Streamable HTTP transport.
- **Dynamic Tool Discovery:** Uses `MultiServerMCPClient` to discover MCP tools.
- **Agent-Based Routing:** LangChain agent selects appropriate tools based on user queries.
- **Cross-Department Queries:** Supports questions requiring information from multiple departments.
- **Safe Calculator:** Performs arithmetic without unrestricted `eval()`.
- **Source Attribution:** Includes document filenames and page numbers.
- **Conversation History:** Maintains contextual conversations using session IDs.
- **Error Handling:** Handles retrieval errors and insufficient evidence.

## Architecture

```text
             User Question
                   |
                   v
            FastAPI Application
                   |
                   v
             LangChain Agent
                   |
                   v
          MultiServerMCPClient
                   |
          +--------+--------+
          |        |        |
          v        v        v
        HR MCP   IT MCP  Finance MCP
        :8001    :8002     :8003
          |        |        |
          v        v        v
       HR RAG   IT RAG   Finance RAG
          |        |        |
          +--------+--------+
                   |
                   v
           Retrieved Evidence
                   |
                   v
           Generated Response
                   |
                   v
             User Response
```

## MCP Servers

| Server | Port | Tools |
|---|---:|---|
| HR | 8001 | `search_hr_documents` |
| IT | 8002 | `search_it_documents` |
| Finance | 8003 | `search_finance_documents`, `calculator` |

The main LangChain agent connects to all three servers through `MultiServerMCPClient` and dynamically registers their discovered tools.

## Technology Stack

- Python and FastAPI
- LangChain and LangChain Agents
- FastMCP and `langchain-mcp-adapters`
- OpenAI LLM and Embeddings
- FAISS / Chroma
- PyPDFLoader
- RecursiveCharacterTextSplitter
- Pydantic
- Postman

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

Start all three MCP servers and the FastAPI application together:

```bash
python run_all.py
```

Alternatively, run each MCP server and Uvicorn separately.

**Main API:** `http://127.0.0.1:8000`

**API Documentation:** `http://127.0.0.1:8000/docs`

## Example API Request

**POST** `/chat`

```json
{
    "session_id": "employee-001",
    "message": "What is the annual leave policy?"
}
```

Use the same `session_id` for follow-up questions to maintain conversation context.

## Testing

The application supports testing of:

- Department-specific document retrieval.
- Multi-department queries.
- Calculator operations.
- Conversation history and follow-up questions.
- Source attribution.
- Insufficient evidence and tool error handling.

## MCP vs Direct Tool Integration

Unlike direct LangChain tool integration, this implementation exposes department functionality through independent MCP servers. The main agent discovers and accesses these tools through a standardized MCP client interface, making the architecture more modular and extensible.