import json

class MCPRBACGateway:
    """
    Secure MCP Server acting as a Knowledge Gateway.
    Implements Role-Based Access Control (RBAC) to prevent Data Leakage
    when LLMs query the internal knowledge base.
    """
    def __init__(self):
        # Mock Vector Database containing documents with security classifications
        self.mock_vector_db = [
            {"id": "doc_1", "text": "CERN Cafeteria menu for July 2026.", "level": "public"},
            {"id": "doc_2", "text": "LHC cooling system standard maintenance manual.", "level": "internal"},
            {"id": "doc_3", "text": "UNDISCLOSED: New antimatter containment parameters.", "level": "secret"}
        ]
        
        # Access control matrix mapping roles to allowed clearance levels
        self.role_clearance = {
            "guest": ["public"],
            "researcher": ["public", "internal"],
            "admin": ["public", "internal", "secret"]
        }

        # Registered tools
        self.tools = {
            "search_documents": self._secure_search
        }

    def _secure_search(self, kwargs):
        """
        Tool logic: Filters search results based on the user's role.
        The LLM MUST provide the user's role token to perform the search.
        """
        query = kwargs.get("query", "").lower()
        user_role = kwargs.get("user_role", "guest") # Default to least privilege

        # 1. Validate the role
        if user_role not in self.role_clearance:
            return {
                "status": "error",
                "error": f"Security Exception: Unknown role '{user_role}'. Access denied."
            }

        allowed_levels = self.role_clearance[user_role]
        results = []

        # 2. Simulate vector search & filter by security clearance
        for doc in self.mock_vector_db:
            if doc["level"] in allowed_levels:
                # Mock search matching logic (in a real app, this is a cosine similarity search)
                if query in doc["text"].lower() or query == "all":
                    results.append({"id": doc["id"], "text": doc["text"], "classification": doc["level"]})

        # 3. Log the access attempt (Crucial for enterprise security audits)
        print(f"[AUDIT LOG] User Role: '{user_role}' | Query: '{query}' | Results Found: {len(results)}")

        return {
            "status": "success",
            "user_role": user_role,
            "results": results
        }

    def execute_tool(self, tool_name, kwargs):
        """Router for MCP tool requests."""
        if tool_name not in self.tools:
            return {"status": "error", "error": "Tool not found."}
        return self.tools[tool_name](kwargs)
