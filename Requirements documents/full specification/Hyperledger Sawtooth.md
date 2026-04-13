# Hyperledger Sawtooth

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Hyperledger Sawtooth and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability and Exception Handling
* 3.2 Information volume and Performance
* 3.3 Developer and Administrator interface
* 3.4 User characteristics
* 3.5 Programming language and architectural constraints
* 3.6 Process requirements



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of a highly scalable, enterprise-grade distributed ledger platform. This system is engineered from the ground up to provide an uncompromising, highly modular blockchain framework that cleanly separates the core system ledger from the application-specific domain logic, enabling organizations to deploy secure, distributed applications in both permissioned and permissionless configurations.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Hyperledger Sawtooth*, and will be referred to as Sawtooth or "the system" in the rest of this document.

The primary purpose of Hyperledger Sawtooth is to serve as a versatile foundation for developing and operating distributed ledger applications and networks. The fundamental architectural philosophy of Sawtooth is the absolute separation of the core consensus and network routing layers from the smart contract execution layer (referred to as Transaction Families). By maintaining this strict separation, Sawtooth allows developers to write application logic in a variety of programming languages without needing to understand the underlying cryptographic peer-to-peer networking, thereby satisfying a broad range of industry use cases natively.

The high-level goals of this new platform instantiation are:
a. To radically decouple transaction semantics from network mechanics by establishing a robust 0.8 REST API and comprehensive 0.8 CLI Tools that interface exclusively through standardized HTTP and ZeroMQ protocols.
b. To introduce an innovative scheduling architecture that provides both Serial and Parallel Schedulers, enabling the concurrent execution of non-conflicting transactions to dramatically increase network throughput.
c. To establish a highly fault-tolerant network messaging backbone by designing network routing to a particular validator and implementing direct send of messages from peer to peer by routing the message across the network topology.
d. To ensure the integrity of the blockchain state by architecting a precise system to implement State Delta Registration with Fork Resolution, allowing nodes to gracefully handle competing blockchain histories.
e. To deliver an unassailable smart contract environment by establishing distinct Transaction Families, such as writing a formal Transaction Family Spec for XO (a reference application) and implementing external identity validation routines.
f. To provide a flawless local development experience by producing updated Developer environment configurations, ensuring developers do not encounter Vagrant installation issues or `vagrant up` failures during network bootstrapping.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the distributed ledger framework's implementation:

* *Arcade* – A specific testing or transaction suite within the Sawtooth ecosystem used to validate transaction integrities.
* *Genesis Block* – The foundational block of the blockchain network. The architecture dictates that startup without initializing genesis data can be highly confusing, demanding that the system enforces clear genesis block initialization.
* *Gossip* – A peer-to-peer communication protocol where nodes randomly share network state with other nodes to ensure eventual consistency.
* *PoET* – Proof of Elapsed Time. Sawtooth's unique consensus algorithm designed to achieve Nakamoto-style consensus without the massive energy consumption of Proof of Work. The system requires a robust 0.8 PoET Simulator for development and testing environments.
* *TP* – Transaction Processor. The application-level component that executes the business logic of a specific Transaction Family.
* *Transaction Family* – A group of operations or transactions that share the same namespace and validation rules.
* *Validator* – The core node daemon responsible for validating transactions, participating in consensus, and managing the Merkle Radix state tree.
* *XO* – A reference Transaction Family implementing the game of Tic-Tac-Toe, used extensively for integration testing and benchmarking. The command-line tool for this family must ensure that the `xo create`'s `--wait` option actively blocks and waits for transaction finality.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the consensus engines, the transaction execution lifecycle, parallel scheduling, and the peer-to-peer interconnect mechanisms. Section 3 mentions other necessary considerations, including strict performance constraints, administrator interfaces, data security mandates, programming constraints (specifically the Go SDK), and deployment packaging requirements.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Validator engine, the Transaction Processors, the database adapters, and the network communication matrix must behave during standard operation and under heavy enterprise transaction load.

### 2.1 Hyperledger Sawtooth and its environment.

The following description outlines the intended relationship between the Hyperledger Sawtooth Validator nodes, the application-specific Transaction Processors, the client SDKs, and the distributed peer network:

* Client applications (written in Go, Python, Java, etc.) submit serialized transactions to the Sawtooth REST API via HTTP POST requests.
* The REST API securely forwards these transactions to the core Validator process. The Validator places the transactions into an internal queue and routes them to the appropriate active Transaction Processor via persistent ZeroMQ (ZMQ) connections.
* The Transaction Processor executes the business logic and calculates the new state. If valid, the Validator updates the global state trie and participates in consensus to finalize the block.
* To support complex network deployments, the architecture must support robust cluster topologies. The development infrastructure must ensure stability so that users are never unable to start a cluster of 2 validators and 2 transaction processors cleanly.
* The internal network engine must continuously evaluate the status of its peers. The system must implement robust Long Running (LR) Networks capabilities to support permanent deployments that do not degrade over time.

The main inputs to Sawtooth come from clients submitting batched transactions, network operators deploying specific Transaction Families, and peer nodes broadcasting consensus messages. It is the job of the Validator's execution engine to continuously analyze these inputs, schedule execution efficiently, manage concurrent state writes, and deliver verified blocks to the immutable ledger.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the distributed ledger framework:

**Transaction Execution and State Management**
a. Hyperledger Sawtooth shall provide an industry-leading, highly concurrent transaction execution engine. The framework must implement a configuration option to select between schedulers dynamically, allowing node operators to choose the optimal path for their specific workloads.
b. When utilizing the advanced execution paths, the architecture team must fully implement state handling in the parallel scheduler branch, ensuring that transactions modifying disjoint state addresses can be evaluated simultaneously without risking state corruption.
c. The communication between the Validator and the Transaction Processors must be highly deterministic. The Validator must reliably send a TP Registration ACK back to the processor before attempting to forward any Transaction Requests, preventing connection race conditions during node startup.
d. State synchronization is paramount for new nodes joining the network. The system must implement State Delta Subscription Catch-up, enabling nodes to rapidly synchronize their local Merkle Radix trees by subscribing directly to state changes rather than replaying every historical transaction.
e. To ensure ecosystem health, the framework must provide robust tools for 0.8 State Export, allowing administrators to generate cryptographically verifiable snapshots of the ledger's state. Furthermore, the system must implement a strict Settings Key Naming Strategy to govern on-chain network configurations.

**Consensus and Cryptographic Primitives**
f. The system shall establish a deeply integrated, hardware-agnostic consensus architecture. For testing environments lacking specialized hardware, the system must provide a simulated Proof of Elapsed Time algorithm. The architecture must resolve missing dependencies to ensure the system does not fail with an `ImportError: No module named poet0_enclave_simulator`.

g. The underlying cryptographic functions must be mathematically sound. The architecture requires dedicated code refactoring around functions such as `generate_identifier(signingkey)` within the `SignedObject` abstractions to guarantee collision resistance and standard compliance.
h. Complex enterprise environments may require distinct chaincode methodologies. The architecture team must support the integration of the Uber chaincode (UC) paradigm into the modular framework.

**Networking and Peer-to-Peer Interconnect**
i. The platform must provide robust network routing capabilities. The Gossip protocol must be resilient against malformed data; the interconnect module must be hardened to fix a critical DEFECT where the interconnect crashes when receiving multipart messages with more than two parts.
j. Advanced routing topologies must be supported. The system must implement the direct send of messages from peer to peer by opening a temporary connection, bypassing standard flooding algorithms for targeted point-to-point data exchange.

**Client SDKs and Development Tooling**
k. The framework must supply highly expressive and reliable SDKs. The 0.8 Go SDK must be fully featured. The Go SDK architecture team must heavily research the Go SDK Distribution Model to ensure it aligns with standard Go package management practices (`go get`).
l. Within the SDKs, stability is a strict mandate. The Go SDK team must resolve the `intkey_go` example issue where an "index out of bound" panic occurs when the network endpoint is not specified, ensuring proper error encapsulation is utilized instead of runtime panics.
m. Network governance requires specialized configuration Transaction Families. The system must fully implement the 0.8 Settings Family to allow dynamic, on-chain updates to network variables (such as max block size or consensus targets).

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, data security policies, and the architectural requirements necessary for an enterprise-grade blockchain deployment.

### 3.1 Reliability and Exception Handling

Reliability of the Validator application layer, the network connections, and the resulting transaction state has a critical priority. The system must guarantee operational stability and security against node crashes and network partitions.

The Validator's execution engine must be incredibly defensive against Transaction Processor instability. The system must be engineered so that the Executor cleanly recovers after a TP crash, automatically un-pairing the crashed process and halting transactions for that family until a new TP reconnects. Furthermore, the Executor must distinguish between application-level failures and protocol-level failures; it must not treat a TP internal error (such as a database timeout) as an "invalid transaction," which would incorrectly permanently reject a valid transaction payload.

The testing environment must enforce strict transaction validation logic. Developers must investigate `is_valid` in the arcade testing suite for transactions that have been maliciously or accidentally altered, and subsequently fix `is_valid` to ensure altered transactions are definitively rejected by the cryptographic signature validation routines.

Network communication mechanisms must be foolproof. The system must guarantee that exceptions are safely caught and logged at the network boundary. The architecture must strictly prevent exceptions from being swallowed silently in `Gossip.start()`, which currently obscures critical initialization failures from the node operators. Additionally, client libraries must respect connection lifecycles; the Go SDK must be updated to ensure it sends a graceful disconnect message to the Validator on a `CTRL-C` termination signal.

### 3.2 Information volume and Performance

The system must be engineered to manage massive datasets consisting of millions of transactions, complex state updates, and continuous peer-to-peer data synchronization.

To monitor the health of high-throughput blockchain networks, the system must provide robust operational telemetry. The architecture must integrate 0.8 Stat Collection, capturing metrics on block validation times, queue depths, and memory consumption to allow enterprise operators to graph the network's performance dynamically.

To guarantee performance at scale, the parallel scheduler relies on Directed Acyclic Graph (DAG) state modeling. By calculating the read/write dependencies of incoming transactions, the scheduler executes disparate state modifications concurrently, only falling back to the Serial scheduler when state dependencies collide. This concurrent design is strictly necessary to satisfy the transaction volume demands of modern enterprise supply chains and financial ledgers.

### 3.3 Developer and Administrator interface

The community of network administrators, smart contract developers, and system integrators requires extensive documentation and logical, predictable configuration interfaces.

The onboarding documentation must be pristine. The technical writing team must Fix the Transaction Family Tutorial to ensure new developers understand the payload serialization processes. Furthermore, they must update the Tutorial Configuration File to reflect the most modern parameters and schemas.

The REST API serves as the primary gateway for client applications. The system must ensure that 0.8 REST API operations are highly observable by requiring the engineering team to create comprehensive logging for the REST API. Furthermore, all documentation relating to this interface must be consolidated; the team is mandated to migrate the REST API Architecture Documentation to Sphinx to maintain rendering consistency with the broader project documentation. For the Go SDK, developers must strictly Document the API utilizing `GoDoc` standards.

Administrative configurations must utilize precise nomenclature. To avoid semantic confusion, the infrastructure scripts must rename the environment variable `CURRENCY` to `SAWTOOTH` to reflect the general-purpose nature of the ledger, rather than implying a cryptocurrency-only application.

### 3.4 User characteristics

The intended users of Hyperledger Sawtooth span from highly technical Go/Python software engineers building custom Transaction Families, to systems administrators deploying Docker and Vagrant-based node clusters.

Because the platform will be deployed globally, its fundamental testing matrices must be rock solid. The quality assurance team must establish a comprehensive suite of negative and positive tests. They must create additional Genesis block test cases to verify the platform initializes correctly under diverse starting conditions. Furthermore, they must evaluate the proposal of participant registration improvement in STL to streamline how new nodes authenticate and join the permissioned network. Lastly, core abstraction utilities like the context manager must be refactored to ensure they definitively pass all unit tests.

### 3.5 Programming language and architectural constraints

The primary programming languages utilized for the underlying execution engine of the Sawtooth platform are Python (for the initial core and certain TPs) and Go (for SDKs and high-performance components). This mandates strict adherence to asynchronous programming paradigms, multi-processing capabilities, and robust binary serialization.

If cryptographic components utilize wait-time distributions (such as in PoET), the system must calculate the target wait time $T$ using exponential distributions mathematically defined as $T = -\ln(r) \times \text{local\_mean}$, where $r$ is a random float between 0 and 1, ensuring fairness in leader election across the node pool.

The deployment and packaging architecture must be meticulously configured to prevent compilation failures. The build system must be rock solid to resolve issues where developers have failed to build `sawtooth-core` from source on standard Linux distributions. To support enterprise distribution, the release engineering team must finalize the 0.8 Deployment Packages (e.g., Debian packages, RPMs) to ensure operators can install the software via standard package managers.

### 3.6 Process requirements

As an enterprise-grade open-source product housed under the Linux Foundation, rigorous organizational governance, documentation, and compliance processes must be fulfilled. The product's value proposition relies entirely on its ability to maintain legal compliance, accurate versioning, and transparent communication with its global community of contributors.

The project repository must accurately reflect its governance structure. The project maintainers are required to rename the `MAINTAINERS` file to `COMMITTERS` to align with the specific open-source governance policies standardized across Hyperledger projects.

Strategic release management is critical. The documentation team must finalize the 0.8 Documentation suite, ensuring all new architectures—such as parallel scheduling, the settings family, and long-running network configurations—are completely documented prior to general availability. Every action—from the compilation of the Go SDK to the exception handling in the Gossip protocol—must be immutably tested, ensuring that the platform meets the strict regulatory and operational requirements of modern enterprise blockchain deployments.
