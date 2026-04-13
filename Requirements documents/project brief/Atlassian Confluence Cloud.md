# Atlassian Confluence Cloud

Atlassian Confluence is a knowledge sharing tool that helps teams create and share content.

1. The enterprise knowledge worker interacts with Atlassian Confluence Cloud via a web-based rich text editor to author and organize corporate documentation.
2. The administrator defines hierarchical "Spaces" and configures granular Role-Based Access Control (RBAC) permissions. The worker creates nested pages within these spaces (up to 10,000 pages per space). The system must natively support Right-to-Left (RTL) languages and allow extended international characters in page titles.
3. Workers author content utilizing dynamic macros (e.g., embedding code blocks with syntax highlighting or rendering Jira issue tables). 
4. The system must actively poll the server via WebSockets or heartbeats to detect if multiple users are editing the same page simultaneously, generating an explicit warning to prevent data overwrites. Real-time, character-by-character collaborative editing (e.g., Google Docs style) is out of scope.
5. The internal search engine continuously indexes page text, attachments, and historical revisions. Users can trigger an asynchronous background task to export an entire space (or specific reordered pages) into a paginated PDF or Docbook format for compliance archiving without blocking the main web application thread.
