# Atlassian Crowd

Atlassian Crowd Atlassian Crowd is a Centralized identity management application.

1. The Identity Access Management (IAM) administrator interacts with Atlassian Crowd via a web-based administration console to configure central authentication policies.
2. The administrator defines a connection to an external corporate directory (such as LDAP or Active Directory). The system synchronizes user identity data into Crowd's internal database cache. Assume the system must process a maximum of 10,000 user records and manage connections for up to 50 downstream applications.
3. Downstream applications (like Jira or Confluence) intercept user login attempts and forward the credentials to the Crowd server via SOAP or REST APIs for validation. 
4. The system hashes the credentials, validates them against the directory cache, and issues a Single Sign-On (SSO) token valid for the entire domain. Advanced OpenID identity provider support for external web federation is out of scope for this version.
5. The system must enforce strict lifecycle management. If the administrator removes a directory connection from the console, the system must instantly cascade the deletion, removing all associated user groups and immediately invalidating any active SSO tokens tied to that directory.
