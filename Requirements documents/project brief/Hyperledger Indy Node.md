# Hyperledger Indy Node

Hyperledger Indy provides tools, libraries, and reusable components for providing digital identities rooted on blockchains or other distributed ledgers so that they are interoperable across administrative domains, applications, and any other silo. Indy is interoperable with other blockchains or can be used standalone powering the decentralization of identity.

1. The identity network administrator deploys a Hyperledger Indy Node by providing a genesis file containing the IP addresses and public keys of the initial validator pool. No graphical user interface is required; configuration is handled entirely via local text files and a command-line interface.
2. The system establishes ZeroMQ (ZMQ) socket connections with the other validator nodes in the pool. It utilizes a Redundant Byzantine Fault Tolerant (RBFT) consensus algorithm to agree on the state of the ledger. For this specification, assume a static pool of exactly 25 validator nodes.
3. An external Identity Authority submits a write request via the network API to publish a new Credential Schema (a JSON structure defining identity attributes) or register a new Decentralized Identifier (DID). The payload must not exceed 10KB.
4. The node validates the cryptographic signature of the incoming request against the sender's previously recorded public key. 
5. If the signature is valid, the node proposes the transaction to the consensus pool, writes it to the local immutable ledger upon agreement, and returns a cryptographic receipt to the sender. Complex key-recovery or credential revocation mechanisms are out of scope for this initial node implementation.
