import json
import sys

file_path = "C:/Users/deept/.claude.json"
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    project_key = "C:/Users/deept"
    if "projects" in data and project_key in data["projects"]:
        if "mcpServers" not in data["projects"][project_key]:
            data["projects"][project_key]["mcpServers"] = {}
        
        data["projects"][project_key]["mcpServers"]["jira-mcp"] = {
            "command": "python",
            "args": ["C:/Users/deept/AIProjects/jira-mcp/server.py"]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Successfully updated .claude.json")
    else:
        print("Project key not found.")
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
