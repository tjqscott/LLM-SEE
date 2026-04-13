# Apache Usergrid

Apache Usergrid is an open-source Backend-as-a-Service composed of an in- tegrated distributed NoSQL database, application layer and client tier with SDKs for developers looking to rapidly build web and/or mobile applications. Apache Usergrid has been developed in Java.

1. The application developer interacts with Apache Usergrid by sending JSON payloads via HTTP REST API endpoints. No client-side graphical dashboard or administrative web UI is required to be built in this initial version.
2. The developer submits requests to define discrete data entities, establish relational connections between them (such as linking a user to a specific activity stream), and execute geospatial or property-based queries. Assume the database stores a maximum of 1 million entities for this testing scenario.
3. The system parses the incoming REST requests, enforces a strict maximum 1MB byte-size limit on the JSON payload to prevent abuse, and validates the incoming authentication token. 
4. Complex Role-Based Access Control (RBAC) hierarchy nesting is out of scope; if a role lacks a defined name string, the system must reject the request with a standard validation exception rather than attempting to inherit permissions.
5. Validated payloads are persisted by the system into a distributed NoSQL database and concurrently indexed into an ElasticSearch cluster to support the property-based queries. 
6. When processing deletion requests, the system must offer a definitive flag to cascade and delete all inbound and outbound connections tied to that entity, preventing orphaned relational records in the graph.
