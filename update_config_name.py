import json
import os
import sys

file_path = r"C:\Users\deept\.gemini\config\mcp_config.json"

try:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if "mcpServers" in data and "jira-mcp" in data["mcpServers"]:
            del data["mcpServers"]["jira-mcp"]
            
        data["mcpServers"]["atlassian-mcp"] = {
            "command": "python",
            "args": ["C:/Users/deept/AIProjects/atlassian-mcp/server.py"]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Successfully updated mcp_config.json")
    else:
        print("mcp_config.json not found")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
