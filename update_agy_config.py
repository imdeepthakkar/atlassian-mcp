import json
import os
import sys

file_path = r"C:\Users\deept\.gemini\config\mcp_config.json"

os.makedirs(os.path.dirname(file_path), exist_ok=True)

try:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"mcpServers": {}}
    else:
        data = {"mcpServers": {}}
    
    if "mcpServers" not in data:
        data["mcpServers"] = {}
        
    data["mcpServers"]["jira-mcp"] = {
        "command": "python",
        "args": ["C:/Users/deept/AIProjects/jira-mcp/server.py"]
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Successfully updated mcp_config.json")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
