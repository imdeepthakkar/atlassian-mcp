import os
import requests
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP("atlassian")

ATLASSIAN_URL = os.environ.get("ATLASSIAN_URL", "https://deepthakkar.atlassian.net")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "deep.thakkar.eu@gmail.com")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
READ_ONLY = os.environ.get("ATLASSIAN_READ_ONLY", "false").lower() == "true"
REQUEST_TIMEOUT = 10

def get_auth():
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        raise ValueError("JIRA_EMAIL and JIRA_API_TOKEN must be available.")
    return (JIRA_EMAIL, JIRA_API_TOKEN)

def assert_write_permitted():
    if READ_ONLY:
        raise PermissionError("Write operations are disabled. Set ATLASSIAN_READ_ONLY=false to enable.")

# --- JIRA TOOLS ---

@mcp.tool()
def get_current_user() -> str:
    """Get the profile of the currently authenticated Jira/Atlassian user."""
    url = f"{ATLASSIAN_URL}/rest/api/3/myself"
    response = requests.get(url, auth=get_auth(), headers={"Accept": "application/json"}, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

@mcp.tool()
def get_projects() -> str:
    """Get a list of all Jira projects."""
    url = f"{ATLASSIAN_URL}/rest/api/3/project"
    response = requests.get(url, auth=get_auth(), headers={"Accept": "application/json"}, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

@mcp.tool()
def search_issues(jql: str = "assignee=currentUser() ORDER BY created DESC", max_results: int = 10) -> str:
    """Search for Jira issues using JQL (Jira Query Language)."""
    url = f"{ATLASSIAN_URL}/rest/api/3/search/jql"
    payload = {
        "jql": jql,
        "maxResults": max_results,
        "fields": ["summary", "issuetype", "status", "description", "assignee"]
    }
    response = requests.post(url, auth=get_auth(), headers={"Accept": "application/json", "Content-Type": "application/json"}, json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

@mcp.tool()
def create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> str:
    """Create a new Jira issue."""
    assert_write_permitted()
    url = f"{ATLASSIAN_URL}/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": description}
                        ]
                    }
                ]
            },
            "issuetype": {"name": issue_type}
        }
    }
    response = requests.post(url, auth=get_auth(), headers={"Accept": "application/json", "Content-Type": "application/json"}, json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

@mcp.tool()
def get_boards(project_key_or_id: str = None) -> str:
    """Get a list of all agile boards. Optionally filter by project key or ID."""
    url = f"{ATLASSIAN_URL}/rest/agile/1.0/board"
    params = {}
    if project_key_or_id:
        params["projectKeyOrId"] = project_key_or_id
    response = requests.get(url, auth=get_auth(), headers={"Accept": "application/json"}, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

@mcp.tool()
def create_sprint(name: str, origin_board_id: int, goal: str = "") -> str:
    """Create a new Sprint for a given board ID."""
    assert_write_permitted()
    url = f"{ATLASSIAN_URL}/rest/agile/1.0/sprint"
    payload = {
        "name": name,
        "originBoardId": origin_board_id
    }
    if goal:
        payload["goal"] = goal
    response = requests.post(url, auth=get_auth(), headers={"Accept": "application/json", "Content-Type": "application/json"}, json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

@mcp.tool()
def update_sprint(sprint_id: int, state: str, start_date: str = None, end_date: str = None) -> str:
    """Update a sprint's state ('active', 'closed', 'future'). To start a sprint, state must be 'active' and start_date/end_date should be provided (ISO 8601 format)."""
    assert_write_permitted()
    url = f"{ATLASSIAN_URL}/rest/agile/1.0/sprint/{sprint_id}"
    payload = {
        "state": state
    }
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date
    response = requests.post(url, auth=get_auth(), headers={"Accept": "application/json", "Content-Type": "application/json"}, json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

# --- CONFLUENCE TOOLS ---

@mcp.tool()
def get_confluence_spaces() -> str:
    """Get a list of all Confluence spaces."""
    url = f"{ATLASSIAN_URL}/wiki/rest/api/space"
    response = requests.get(url, auth=get_auth(), headers={"Accept": "application/json"}, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

@mcp.tool()
def search_confluence(cql: str, limit: int = 10) -> str:
    """Search Confluence using CQL (Confluence Query Language)."""
    url = f"{ATLASSIAN_URL}/wiki/rest/api/search"
    params = {
        "cql": cql,
        "limit": limit
    }
    response = requests.get(url, auth=get_auth(), headers={"Accept": "application/json"}, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

@mcp.tool()
def get_confluence_page(page_id: str) -> str:
    """Get the content of a specific Confluence page by its ID."""
    url = f"{ATLASSIAN_URL}/wiki/rest/api/content/{page_id}?expand=body.storage"
    response = requests.get(url, auth=get_auth(), headers={"Accept": "application/json"}, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    mcp.run(transport='stdio')
