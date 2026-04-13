# Hyperledger Blockchain Explorer

Hyperledger Explorer is a user-friendly Web appli- cation tool used to view, invoke, deploy or query blocks, transactions and associated data, network information (name, status, list of nodes), chain codes and transaction families, as well as any other relevant information stored in the ledger.

1. The network operator configures the Hyperledger Blockchain Explorer by providing connection credentials (peer endpoints, TLS certificates) to an underlying Hyperledger Fabric network via a local JSON configuration file.
2. Upon startup, the system connects to the Fabric network and listens for new block events via WebSockets. 
3. It parses incoming blocks, extracting transaction details, channel metrics, and chaincode executions, and persists this data into a local relational database (e.g., PostgreSQL). Assume the system will process and store a maximum of 100,000 blocks.
4. The system renders a web-based graphical dashboard displaying aggregated metrics, such as blocks per hour, active nodes, and transaction volume. The web interface must auto-refresh without requiring manual page reloads.
5. The operator can search for specific blocks or transactions using their unique hash IDs through the dashboard search bar. Initiating new blockchain transactions or altering network configurations directly from this web interface is strictly out of scope; the system is entirely read-only.
