# CERN Safe AI: Secure RBAC Knowledge Gateway

An intelligent Model Context Protocol (MCP) server that acts as a secure knowledge gateway, designed to prevent **Data Leakage** when Large Language Models query internal databases.

This project addresses the core data governance challenges faced by enterprise IT departments, ensuring that AI agents respect strict data privacy and security classifications without relying on the LLM itself to filter sensitive information.

## The Challenge: Data Governance & Privacy
Deploying Large Language Models in a complex research environment requires robust data governance, as outlined in the ["General principles for the use of AI at CERN"](https://home.cern/general-principles-use-ai-cern/). A major obstacle is the risk of Data Leakage—where an AI model inadvertently exposes sensitive information. To comply with CERN's principles, systems must enforce strict access controls without relying on the LLM's internal alignment:

> *"Security and safety: AI must be adequately protected... Data privacy: AI must be used in a manner that respects privacy and the protection of personal data."*

## The Solution

This project implements a secure **MCP Gateway** that enforces Role-Based Access Control (RBAC) at the server level, fully decoupling the security logic from the AI model:

1. Identity & Role Extraction: The local LLM parses natural language to autonomously deduce the user's authorization role (e.g., Guest vs. System Admin).
2. Server-Side Enforcement: The MCP server receives the role alongside the query and strictly filters the mock Vector Database based on clearance levels (`public`, `internal`, `secret`).
3. Audit Logging: Every data access attempt by the AI is logged with the user's role and query for complete traceability.

## Project Structure

* `mcp_rbac_gateway.py`: The core MCP server containing the RBAC matrix, the mock document database, and the filtering logic.
* `ollama_rbac_agent.py`: An integration script using a local LLM (Llama 3.2 via Ollama) to demonstrate identity extraction and role-based tool calling.
* `test_mock_rbac.py`: A dependency-free simulation script to evaluate the RBAC filtering and server logic instantly without an LLM.

---

## Getting Started

You can test this architecture in two ways: using a real local AI or running a rapid dependency-free mock test.

### Option A: Run with Real AI (Requires Ollama)

This demonstrates a live LLM extracting user roles from natural language prompts and passing them to the secure gateway.

Prerequisites:

* Python 3.9+
* Ollama installed and running locally with `llama3.2`.
* `pip install ollama`

Execution:

```bash
python ollama_rbac_agent.py
```

Live Output:

```text
Testing local Llama 3.2 against RBAC Gateway 

User speaking to AI: Alice
LLM is calling Tool: 'search_documents' with args: {'query': 'all', 'user_role': 'guest'}
[AUDIT LOG] User Role: 'guest' | Query: 'all' | Results Found: 1
Server Filtered Response:
{
  "status": "success",
  "user_role": "guest",
  "results": [
    {
      "id": "doc_1",
      "text": "CERN Cafeteria menu for July 2026.",
      "classification": "public"
    }
  ]
}
--------------------------------------------------

User speaking to AI: Eve
LLM is calling Tool: 'search_documents' with args: {'query': 'all', 'user_role': 'admin'}
[AUDIT LOG] User Role: 'admin' | Query: 'all' | Results Found: 3
Server Filtered Response:
{
  "status": "success",
  "user_role": "admin",
  "results": [
    {
      "id": "doc_1",
      "text": "CERN Cafeteria menu for July 2026.",
      "classification": "public"
    },
    {
      "id": "doc_2",
      "text": "LHC cooling system standard maintenance manual.",
      "classification": "internal"
    },
    {
      "id": "doc_3",
      "text": "UNDISCLOSED: New antimatter containment parameters.",
      "classification": "secret"
    }
  ]
}
```

### Option B: Run Dependency-Free Mock Test

If you want to evaluate the RBAC filtering matrix and the audit logging mechanism instantly without installing AI models, use the mock test.

Execution:

```bash
python test_mock_rbac.py
```

## Tech Stack

* Language: Python 3 (Standard Library for core server)
* AI Integration: Ollama API (Llama 3.2)
* Architecture: Model Context Protocol (MCP), Role-Based Access Control (RBAC), AI Identity Extraction
