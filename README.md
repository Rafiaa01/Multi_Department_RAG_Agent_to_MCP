# Multi-Department RAG Agent

An intelligent internal assistant built with **Python, FastAPI, LangChain, and LLM-powered agents**. The assistant answers employee questions using separate HR, IT Support, and Finance policy documents. It dynamically selects the appropriate department tools, retrieves supporting evidence, performs safe calculations, and maintains conversation history.

## 1. Project Overview

The Multi-Department RAG Agent provides a unified interface for employees to ask questions across different company departments.

Unlike a traditional RAG pipeline that follows a fixed retrieval process, this application uses an AI agent to decide which tools are required to answer a question.

The agent can:

- Retrieve information from HR policy documents.
- Search IT Support documentation.
- Retrieve Finance policy information.
- Use multiple department tools for cross-department questions.
- Perform arithmetic calculations using a safe calculator.
- Ask follow-up questions when a request is ambiguous.
- Maintain conversation history for contextual responses.
- Provide document names and page numbers as evidence.
- Handle missing information and tool execution errors.

## 2. Key Features

| Feature | Description |
|---|---|
| Multi-department RAG | Separate retrieval tools for HR, IT, and Finance. |
| Agent-based routing | The agent selects the appropriate tool based on the user's question. |
| Cross-department retrieval | Supports questions requiring evidence from multiple departments. |
| Safe calculator | Performs arithmetic without unrestricted `eval()`. |
| Source attribution | Includes document names and page numbers in factual answers. |
| Relevance checking | Checks retrieved documents before using them as evidence. |
| Clarification | Requests additional details when a question is ambiguous. |
| Conversation history | Maintains context across follow-up questions. |
| Error handling | Handles tool failures without crashing the application. |
| Execution limits | Restricts repeated tool calls to prevent unnecessary execution. |

## 3. Architecture

The application follows an agentic RAG architecture.

```text
                  User Question
                        |
                        v
                 FastAPI Endpoint
                        |
                        v
                  AI Agent (LLM)
                        |
              Understand User Intent
                        |
           +------------+------------+
           |            |            |
           v            v            v
        HR Tool       IT Tool     Finance Tool
           |            |            |
           v            v            v
       HR Vector    IT Vector    Finance Vector
        Store         Store        Store
           |            |            |
           +------------+------------+
                        |
                        v
                Retrieved Evidence
                        |
                Relevance Checking
                        |
              +---------+---------+
              |                   |
              v                   v
          Calculator        Missing/Weak
              |               Evidence
              |                   |
              +---------+---------+
                        |
                        v
                 Agent Generates
                    Response
                        |
                        v
              Sources and Page Numbers
                        |
                        v
                 User Response
```

## 4. Department Retrieval Tools

Each department has its own document collection and retrieval tool.

### HR Department

`search_hr_documents(query)`

Retrieves information related to:

- Annual leave
- Sick leave
- Working hours
- Remote work
- Probation policies

### IT Support Department

`search_it_documents(query)`

Retrieves information related to:

- IT equipment
- Laptop requests
- Software installation
- Technical support
- Access and security policies

### Finance Department

`search_finance_documents(query)`

Retrieves information related to:

- Expense reimbursement
- Department budgets
- Purchase policies
- Employee allowances
- Financial approvals

Each retrieval tool returns relevant document chunks along with their source document names and page metadata.

## 5. Safe Calculator Tool

The application includes a calculator tool for arithmetic questions.

Examples:

- Calculate the total cost of multiple IT purchases.
- Calculate an expense reimbursement amount.
- Calculate the remaining budget after expenses.

The calculator uses restricted arithmetic operations rather than unrestricted Python `eval()`.

## 6. Agent Decision-Making

The agent determines which tools are required based on the user's request.

For example:

| User question | Expected tool selection |
|---|---|
| How many annual leave days are allowed? | HR |
| How can I request a laptop? | IT |
| What is the reimbursement policy? | Finance |
| Can I purchase a monitor using my department budget? | IT + Finance |
| What is the total cost of three laptops at $800 each? | Calculator |
| What is the company policy? | Ask for clarification |

The agent can use multiple tools when a question requires information from different departments.

## 7. Relevance Checking and Grounded Responses

Retrieved documents are checked for relevance before being used to generate an answer.

The application uses a retrieval threshold or relevance-checking mechanism to reduce irrelevant evidence.

The agent follows these rules:

- Answer factual questions using retrieved policy evidence.
- Include source document names and page numbers.
- Do not invent missing policy information.
- Acknowledge when retrieved documents do not establish an answer.
- Ask for clarification when the user's request is ambiguous.

## 8. Conversation History

The application maintains conversation history using session IDs.

Each session stores its own conversation messages, allowing the agent to understand follow-up questions.

Example:

**First question:**

"How can I request a company laptop?"

**Follow-up question:**

"Can I purchase it myself?"

The agent uses the previous conversation to understand what "it" refers to and can retrieve relevant IT and Finance policies.

## 9. Error Handling and Execution Limits

The application includes safeguards to improve reliability:

- Handle retrieval tool errors without terminating the application.
- Handle calculator errors safely.
- Return a controlled response when a tool fails.
- Limit the number of agent tool calls per request.
- Prevent unnecessary repeated retrieval calls.
- Acknowledge when the available evidence is insufficient.

## 10. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API |
| LangChain | Agent and RAG orchestration |
| LLM | Reasoning and tool selection |
| FAISS / Chroma | Vector storage and retrieval |
| Embeddings | Convert policy documents into vectors |
| PyPDFLoader | PDF document loading |
| RecursiveCharacterTextSplitter | Document chunking |
| Pydantic | Request and response validation |
| Postman | API testing |
