# MongoDB Compass

MongoDB Compass provides quick visualization of the structure of data in the database, and perform ad hoc queries ? all with zero knowledge of Mon- goDB?s query language.

1. The database administrator connects to a remote MongoDB cluster by inputting a standard connection URI string into the MongoDB Compass graphical desktop application. Connecting via SSL/TLS certificates or advanced LDAP authentication is out of scope.
2. Upon connection, the system queries the cluster and displays a hierarchical list of available databases and their nested collections. Assume a maximum of 10 databases and 100 collections per database.
3. The administrator selects a specific collection. The system automatically executes a randomized sampling query (fetching a maximum of 1,000 documents) to analyze the schema.
4. The system parses the sampled documents, infers data types (e.g., String, Int32, Date), and renders a visual dashboard displaying the frequency and distribution of these fields without requiring the administrator to write raw MongoDB Query Language (MQL) syntax. 
5. Real-time, continuous schema monitoring of incoming writes is out of scope; the analysis is a point-in-time snapshot.
