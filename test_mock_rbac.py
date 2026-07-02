import json
from mcp_rbac_gateway import MCPRBACGateway

def simulate_llm_queries():
    """
    Simulates an LLM querying the Knowledge Gateway on behalf of different users.
    Demonstrates that the MCP server successfully prevents data leakage.
    """
    server = MCPRBACGateway()
    
    # The LLM attempts to fetch all documents for three different users
    test_cases = [
        {"user": "Alice (Public Guest)", "role": "guest", "query": "all"},
        {"user": "Bob (CERN Researcher)", "role": "researcher", "query": "all"},
        {"user": "Eve (System Admin)", "role": "admin", "query": "all"},
        {"user": "Mallory (Hacker)", "role": "super_hacker", "query": "all"} # Unknown role
    ]

    print("=== Initiating LLM Data Leakage Prevention Test ===\n")

    for case in test_cases:
        print(f"👤 LLM executing search for: {case['user']}")
        
        # The agent MUST pass the user_role to the tool
        arguments = {"query": case["query"], "user_role": case["role"]}
        
        # Execute tool
        response = server.execute_tool("search_documents", arguments)
        
        # Print results safely
        print(f"🔒 Server Response:")
        print(json.dumps(response, indent=2))
        print("-" * 50 + "\n")

if __name__ == "__main__":
    simulate_llm_queries()
