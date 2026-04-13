# Atlassian Bamboo

Atlassian Bamboo Bamboo is a continuous integration and continuous deployment server developed by Atlassian.

1. The release manager interacts with Atlassian Bamboo via a web-based dashboard to configure automated continuous integration pipelines.
2. The manager defines a connection to an external source control repository (such as CVS or Subversion) using secure, obfuscated credentials. 
3. The system's internal change detector continuously polls the repository for new commits. This polling engine must operate asynchronously in a dedicated queue to prevent locking the main Java web interface. Assume the system manages a maximum of 50 concurrent build plans.
4. Upon detecting a source code change, the system allocates a build task to a distributed builder process. The builder executes custom Bash scripts or Maven commands to compile the code. Orchestrating dynamic Docker containers to act as ephemeral build agents is out of scope; assume all builders execute directly on static host operating systems.
5. Upon completion, the system stores the resulting binary artifacts on the local file system and generates notification payloads. The system must dispatch these notifications via Email and Jabber (XMPP) to the development team, while rendering a complete, searchable build log on the public web dashboard.
