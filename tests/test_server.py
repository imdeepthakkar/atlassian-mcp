import pytest
import responses
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import server

@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    # Mock module-level variables since they are evaluated at import time
    monkeypatch.setattr(server, "JIRA_EMAIL", "test@example.com")
    monkeypatch.setattr(server, "JIRA_API_TOKEN", "fake_token")
    monkeypatch.setattr(server, "ATLASSIAN_URL", "https://test.atlassian.net")
    
    # Reset READ_ONLY state
    server.READ_ONLY = False

def test_get_auth():
    assert server.get_auth() == ("test@example.com", "fake_token")

@responses.activate
def test_get_current_user():
    responses.add(
        responses.GET,
        "https://test.atlassian.net/rest/api/3/myself",
        json={"accountId": "123", "displayName": "Test User"},
        status=200
    )
    result = server.get_current_user()
    assert "Test User" in result

def test_read_only_mode(monkeypatch):
    # Set read only flag
    server.READ_ONLY = True
    
    with pytest.raises(PermissionError, match="Write operations are disabled"):
        server.assert_write_permitted()
    
    with pytest.raises(PermissionError):
        server.create_issue("TEST", "Summary", "Description")
        
    # Reset
    server.READ_ONLY = False
