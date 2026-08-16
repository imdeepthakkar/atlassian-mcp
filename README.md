# 🚀 Atlassian FastMCP Server 🛠️

Welcome to the **Atlassian FastMCP Server**! 🌟 This project is a blazingly fast, lightweight Model Context Protocol (MCP) server that seamlessly integrates Atlassian tools like **Jira** and **Confluence** directly into your AI workflows! 🤖✨

---

## 🎯 What does this do?

This MCP server provides a set of highly useful tools that allow AI agents to manage your Atlassian ecosystem effortlessly. From fetching current profiles to creating sprints and generating tickets, this server brings agile management straight to your fingertips! 🖐️💻

### 🛠️ Available Tools

#### 📝 Jira Management
- **`get_current_user`** 👤: Fetch the profile of the currently authenticated Jira/Atlassian user.
- **`get_projects`** 🗂️: Get a beautiful list of all Jira projects in your workspace.
- **`search_issues`** 🔍: Run powerful JQL (Jira Query Language) queries to find exactly the tickets you need!
- **`create_issue`** ➕: Quickly spin up new tasks, stories, or bugs directly in a specified project!

#### 🏃‍♂️ Agile & Sprint Operations (NEW! 🎉)
- **`get_boards`** 📋: Fetch agile boards (with optional filtering by project key) to find where your sprints live!
- **`create_sprint`** 🏃: Generate a brand new Sprint for your team's board, complete with custom goals! 🥅
- **`update_sprint`** 🔄: Manage your sprint's lifecycle! Start an active sprint with start/end dates, or close out a finished one! 🏁

#### 📚 Confluence Knowledge Base
- **`get_confluence_spaces`** 🌌: Discover all the knowledge spaces available in your Confluence instance.
- **`search_confluence`** 🕵️‍♂️: Use CQL (Confluence Query Language) to find documents, meeting notes, and specs.
- **`get_confluence_page`** 📄: Pull the rich content (body storage) of any specific Confluence page by its ID!

---

## 🔐 Setup & Authentication 🗝️

To get this bad boy running, you need to provide your Jira credentials. The server looks for your credentials in two ways:

1. **Environment Variables** 🌐 (Recommended for production):
   - `JIRA_EMAIL` 📧: Your Atlassian account email.
   - `JIRA_API_TOKEN` 🔑: Your Atlassian API Token.

2. **Local Key File** 📁 (Great for local dev):
   - Place a file named `JIRA_KEY.txt` in `C:\Users\deept\AIProjects\Atlassian\` containing your raw API token. 
   - *(Note: This file is safely ignored by Git! 🤫)*

---

## 🚀 Running the Server

Make sure you have your dependencies installed:
```bash
pip install -r requirements.txt
```

Then, fire up the server! 🔥
```bash
python server.py
```
*The server will start up and listen on standard input/output (`stdio`) for fast, secure MCP communication!* 🚄

---

## 🤝 Contributing & Updates

Want to add more Jira magic? 🧙‍♂️ Feel free to fork, update `server.py`, and run the included `update_config.py` scripts to sync your fresh tools! 

Happy building! 👷‍♀️🎉
