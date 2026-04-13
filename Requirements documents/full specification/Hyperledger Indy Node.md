# Hyperledger Indy Node

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Hyperledger Indy Node and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability and Security
* 3.2 Information volume and Performance
* 3.3 Developer and Administrator interface
* 3.4 User characteristics
* 3.5 Programming language and architectural constraints
* 3.6 Process requirements



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of a highly scalable, enterprise-grade distributed ledger purpose-built for decentralized identity. This system is engineered from the ground up to provide the tools, libraries, and reusable components necessary for rooting digital identities on blockchains so that they are interoperable across administrative domains, applications, and organizational silos.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Hyperledger Indy Node*, and will be referred to as Indy or "the system" in the rest of this document.

The primary purpose of Hyperledger Indy Node is to power the decentralization of identity. In the current digital landscape, identity is siloed; users are forced to create hundreds of usernames and passwords across centralized databases that act as honeypots for hackers. Hyperledger Indy aims to establish a sovereign identity ecosystem where individuals and organizations control their own data. Indy is designed to be interoperable with other blockchains or can be used as a standalone network powering a global public utility for identity.

The high-level goals of this new platform instantiation are:
a. To radically democratize digital identity by implementing robust, native DID/DDO support (Decentralized Identifiers and DID Descriptor Objects) directly into the ledger's core data model.
b. To provide uncompromising privacy for users by implementing Anoncreds (Anonymous Credentials), utilizing zero-knowledge proofs to allow users to prove claims about themselves without revealing underlying sensitive data.
c. To establish a highly secure and resilient consensus mechanism that can withstand malicious nodes. The architecture must guarantee that the network can survive adverse conditions, ensuring the pool is fully functional even when dealing with a bad network of 2-second latency and 20% dropped packets.
d. To ensure robust security practices are embedded in the foundation, explicitly mandating that the ThreatModel strictly prohibits Validator Private Keys from being world-readable, ensuring cryptographic material is locked down at the OS level.
e. To deliver an unassailable data storage layer by mandating that the system use `ChunkedFileStorage` for transactions in the Ledger, allowing the node to scale to billions of identity transactions without exhausting memory.
f. To provide granular, enterprise-grade identity interactions by generating verifiable Consent Receipts, giving users cryptographic proof of exactly what data they agreed to share and with whom.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the identity ledger's implementation:

* *Anoncreds* – Anonymous Credentials. A privacy-preserving credential format that allows for zero-knowledge proofs.
* *CII Badge* – Core Infrastructure Initiative Best Practices badge. The project is mandated to achieve a CII badge to demonstrate its commitment to open-source security standards.
* *DDO* – DID Document Object. A JSON-LD object that contains the public keys and service endpoints associated with a DID.
* *DID* – Decentralized Identifier. A globally unique identifier that does not require a centralized registration authority.
* *Plenum* – The underlying Byzantine Fault Tolerant (BFT) consensus protocol that Indy utilizes to order transactions.
* *PRNG* – Pseudo-Random Number Generator. The architecture strictly dictates that the system must not use Pseudo Random Number Generators in the Sovrin-Common and State subprojects, mandating cryptographically secure randomness instead.
* *ZMQ* – ZeroMQ. A high-performance asynchronous messaging library aimed at use in distributed or concurrent applications. Indy nodes utilize ZMQ for peer-to-peer gossip and consensus messages.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the identity data structures, the consensus mechanisms, the zero-knowledge proof integrations, and the peer-to-peer network routing. Section 3 mentions other necessary considerations, including strict performance constraints, administrator interfaces, data security mandates, cryptographic constraints, and deployment packaging requirements.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core node engine, the consensus voting algorithms, the database storage adapters, and the client communication matrix must behave during standard operation and under heavy enterprise transaction load.

### 2.1 Hyperledger Indy Node and its environment.

The following description outlines the intended relationship between Hyperledger Indy nodes, the client SDKs, the validator pools, and the underlying file systems:

* Client applications (wallets, agents) submit identity transactions (like DID creation or schema publishing) to the Indy Node pool via ZMQ sockets. The system's `ClientZStack` must be highly resilient, ensuring it has a provision to cleanly disconnect a client when the transaction is completed or the session times out.
* Inside the node pool, transactions are ordered using the Plenum consensus protocol. During consensus, nodes must validate every incoming message rigorously. The architecture demands the engineering team build a dedicated validation component used to validate every incoming message to a node, verifying cryptographic signatures before deserialization.
* To support massive identity rollouts with high throughput, the architecture must support robust data synchronization. The node must monitor its peers continuously. A node should automatically start the catch-up process if it realizes that it has lagged behind the other nodes in the network.
* The nodes store their immutable state to the local disk. When interacting with the file system, the installation process must be careful with permissions; specifically, installing the client as root must not lock the files, but rather allow the standard application users to access the transaction files seamlessly.

The main inputs to Indy come from agents submitting schemas, credential definitions, and node operators adjusting the validator pool. It is the job of the system's execution engine to continuously analyze these inputs, manage concurrent ZMQ streams, validate complex cryptographic proofs, and append the finalized state to the immutable chunked ledger efficiently.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the decentralized identity framework:

**Consensus, State Management, and Node Lifecycle**
a. Hyperledger Indy Node shall provide a highly extensible and mathematically rigorous consensus architecture. The consensus state machine must be absolute. The architecture requires that the `Pre-Prepare` consensus phase needs to have both the pre-state root and the post-state root embedded within the message. Furthermore, reverting the state root needs to happen reactively if a consensus round fails.

b. The system must aggressively protect network stability through peer evaluation, employing Blacklisting for nodes that send malformed requests. However, this must be finely tuned; a blocking issue must be avoided where, under high load from performance tests, the nodes blacklist each other so no consensus can happen.
c. The node demotion and promotion lifecycle must be seamless. The `send NODE` command must be thoroughly validated to ensure node demotion is never broken because of missing parameters.
d. To ensure a distributed network does not fragment, the architecture team must analyze attack vectors in the catchup process, preventing malicious peers from feeding a lagging node an alternative, invalid history. Furthermore, the system must resolve any vulnerability where slow nodes can be stalled indefinitely after a view change.

**Decentralized Identity and Credentials**
e. The platform shall serve as the root of trust for digital identity. It must natively support DID/DDO data structures, acting as a decentralized public key infrastructure (DPKI).
f. Privacy preservation is a core functional requirement. The system must implement Anoncreds, providing the ledger-side components (Schemas, Credential Definitions, and Revocation Registries) required to verify zero-knowledge proofs.

g. The system must promote interoperability across domains. The architecture must implement robust Anchoring capabilities, allowing the Indy ledger's state to be periodically anchored to other major blockchains (like Bitcoin or Ethereum) for secondary finality.
h. To assist developers in building applications on top of the ledger, the core project must provide a reference Demo Agent that demonstrates best practices for DID authentication and credential exchange.

**Message Validation and Protocol Commands**
i. The system shall establish a deeply integrated transaction validation architecture. Input validation is paramount. The system must implement strict node-to-node messages validation to prevent malicious payloads from traversing the ZMQ network.
j. Administrative protocol commands must be strictly parsed. For the `send NODE` command, the architecture dictates that the parameter `data.alias` and the parameter `data.services` are validated properly before processing. The `data.services` parameter must be strictly mandatory, and the `data` parameter itself must not permit unknown fields, rejecting the transaction if unexpected data is found.
k. The genesis block is the foundation of the network's trust. The initialization scripts must include input validation tests ensuring that the genesis txn file never defines the same key more than once.
l. Client interaction must be supported natively. The protocol must fully support the commands `send GET_ATTR` and `send GET_SCHEMA` to allow edge agents to query public identity structures.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, data security policies, and the Python architectural requirements necessary for a global decentralized deployment.

### 3.1 Reliability and Security

Reliability of the node layer, the ZMQ network connections, and the resulting cryptographic proofs has a critical priority. The system must guarantee operational stability and security against malicious actors and misconfigurations.

Identity key management must be completely foolproof. A critical security ThreatModel mandate dictates that Sovrin CLI Keyring files must never be world-readable and must have strong encryption security applied at rest. Similarly, the Validator Private Keys must be locked down to prevent node impersonation.

The cryptographic transport layer requires strict adherence to mathematical standards. The engineering team must definitively ban the use of Pseudo Random Number Generators (PRNG) in the Sovrin-Common and State subprojects, replacing them with hardware-backed or cryptographically secure random sources to prevent key prediction attacks.

Data integrity at the storage layer must be robust. The system must implement specific fault-tolerance routines to find out if the node is able to handle a corrupt ledger record gracefully, potentially isolating the corrupted chunk and recovering the state from peer nodes.

When roles and permissions are evaluated, the system must not fail silently. When one role has not enough permissions for an action, the corresponding error text returned to the client should be exceptionally clear, outlining exactly which RBAC (Role-Based Access Control) policy was violated.

### 3.2 Information volume and Performance

The system must be engineered to manage massive datasets consisting of millions of identity transactions and credential definitions.

To support high-throughput identity verification, the network must be optimized for speed. The system must implement intelligent Batching mechanisms, grouping multiple identity transactions into a single consensus payload to maximize network utilization. Furthermore, the system architecture requires that the transaction size be strictly limited to prevent bloat attacks from filling the ledger with massive, un-prunable data blobs.

Network health monitoring must be proactive. The internal performance Monitor needs to specifically compensate for extra work done by the master's replicas, ensuring that the primary node is not falsely penalized for the overhead associated with leading the consensus round.

Storage scaling requires intelligent file mapping. The mandate to use `ChunkedFileStorage` for transactions ensures that the ledger can grow indefinitely across multiple physical disks without requiring the entire history to be mapped into contiguous virtual memory.

### 3.3 Developer and Administrator interface

The community of network administrators, identity developers, and system integrators requires extensive documentation and highly predictable CLI interfaces.

The command-line interface must be resilient to human error. The system must guarantee that the Client CLI does not crash or fail when handling a whitespace character in the `pool_transaction_file` path. Furthermore, the CLI must never crash when sending the `SCHEMA` command, ensuring a smooth experience for credential issuers.

String parsing must be universally compatible. The system must be engineered to flawlessly accept non-utf8 characters without throwing a fatal `UnicodeDecodeError: 'utf-8' codec can't decode byte`, ensuring international names and metadata are preserved.

Network errors must be transparent. The architecture must ensure that proper error messages are surfaced when a TCP connection is not available for ZMQ, rather than hanging indefinitely.

Upgrades must be fully supported. The engineering team must build a robust migration script mechanism to ensure data continuity between major protocol versions. The system must explicitly guarantee that node operators are able to seamlessly upgrade from legacy stable versions (e.g., from Stable 0.3.7 to Stable 0.3.13) without requiring a complete ledger rebuild.

### 3.4 User characteristics

The intended users of Hyperledger Indy Node span from highly technical Python/C++ software engineers building custom identity agents to DevOps administrators provisioning massive Linux-based validator pools.

Because the platform will be deployed as public utility infrastructure, its installation and operation must be standardized. The team must improve the OSCAP template specifically for Ubuntu 16.04 nodes to streamline enterprise deployments. Furthermore, the architecture must guarantee cross-platform daemon stability, resolving any underlying core library issues that cause the client to crash on Ubuntu 17.04 or CentOS distributions.

### 3.5 Programming language and architectural constraints

The primary programming language utilized for the underlying execution engine of the Indy Node platform is Python, heavily reliant on C-bindings for cryptography and ZMQ networking. This mandates strict adherence to asynchronous programming paradigms, memory management, and robust exception handling.

The testing pipeline must be rigorously expanded to ensure continuous stability. The quality assurance team is mandated to create negative unit-level tests to ensure the node handles malicious payloads correctly. Furthermore, the CI pipeline must be optimized to resolve the intermittent failure of Plenum's tests, ensuring that flakiness does not block critical PR merges.

### 3.6 Process requirements

As an enterprise-grade open-source project transitioning into the Linux Foundation, rigorous organizational onboarding, documentation, and compliance processes must be fulfilled. The product's value proposition relies entirely on its ability to foster a massive, collaborative open-source community.

The onboarding process must be welcoming and structured. The documentation team is mandated to create a comprehensive "WELCOME TO INDY!" guide for new contributors. To maintain issue tracker hygiene, the project must explicitly document "How to log a good Indy bug" so that community reports contain actionable diagnostic data.

As the original codebase (formerly known as Sovrin) is migrated, strict administrative alignment is required. The infrastructure team must merge the appropriate PRs and redeploy `sovrin.org` to correct the link to the Global State Table (GST). Furthermore, organizational migration requires that the original Sovrin Project team (using the Evernym Jira "SOV" project) successfully log into Hyperledger's Jira and officially comment on their migration stories to verify their new accounts. Every action must ensure that the platform meets the strict regulatory, security, and operational requirements necessary to build the world's premier decentralized identity network.