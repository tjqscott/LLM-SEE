# Hyperledger Blockchain Explorer

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Hyperledger Blockchain Explorer and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and database performance
* 3.3 Developer and Administrator interface
* 3.4 User characteristics
* 3.5 Programming language and architectural constraints
* 3.6 Process requirements



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of a highly scalable, enterprise-grade blockchain monitoring and analytics platform. This system is engineered from the ground up to provide a centralized, secure, and highly extensible environment for network operators and developers to visualize the underlying mechanics of distributed ledger technologies without needing to interact with complex command-line interfaces or raw RPC streams.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Hyperledger Blockchain Explorer*, and will be referred to as the Explorer or "the system" in the rest of this document.

The primary purpose of the Hyperledger Blockchain Explorer is to act as a user-friendly Web application tool used to view, invoke, deploy or query blocks, transactions and associated data, network information (name, status, list of nodes), chain codes and transaction families, as well as any other relevant information stored in the ledger. In the current enterprise blockchain landscape, administrators struggle to gain real-time visibility into the health and transaction volume of their networks. The Explorer aims to establish a unified digital workspace where network transparency is democratized, and application delivery is standardized through a highly modular architecture.

The high-level goals of this new platform instantiation are:
a. To radically democratize blockchain visibility by mandating the engineering team to implement a generic blockchain explorer which can work with any Blockchain platform, rather than being strictly tightly coupled to a single protocol.
b. To provide an uncompromising, real-time data visualization experience by implementing live statistics in the Blockchain explorer using websockets protocol and a POSTGRES DB.
c. To establish a highly secure, modular backend architecture by implementing a Node JS web server using Express, alongside the implementation of dynamic module load needed for each Blockchain implementation.
d. To ensure seamless interoperability with the broader Hyperledger ecosystem by aggressively pursuing an initiative to create enhancements to Blockchain Explorer compatible with Fabric V 1.0.
e. To deliver an unassailable deployment and orchestration experience, ensuring the platform can easily enable docker image building and use official hyperledger images in the blockchain explorer docker-compose files to establish trust and reliability during initial provisioning.
f. To provide granular, enterprise-grade access control and interaction by providing the ability to add a channel from the Web UI directly, ensuring network operators can partition data seamlessly.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the blockchain explorer's implementation:

* *Chaincode* – The smart contract logic deployed on a Hyperledger Fabric network. The Explorer must be able to query and invoke these programs.
* *Fossology* – An open-source license compliance software system and toolkit. The development team is mandated to resolve licensing issues discovered by Fossology scans to ensure compliance with the Apache 2.0 license.
* *gRPC* – A high-performance, open-source universal RPC framework. The Explorer utilizes this to communicate with peer nodes.
* *MIP* – Modular Implementation Protocol or related sub-project. The documentation team must add information about the new MIP blockchain explorer to the base Blockchain Explorer repository README.
* *Orderer* – The node responsible for packaging transactions into blocks and distributing them to peers. The architecture must natively support the Node SDK for chain create phase 1 to submit to the Orderer.
* *TSC* – Technical Steering Committee. The governing body of the Hyperledger project. The release of this software is strictly gated upon TSC Approval to publish Blockchain Explorer 0.3 to the HL Open Source Community.
* *WebSockets* – A computer communications protocol providing full-duplex communication channels over a single TCP connection, strictly required for the platform's real-time statistical updates.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the web interfaces, the backend data ingestion engines, the Docker orchestration, and the generic platform abstraction layers. Section 3 mentions other necessary considerations, including strict performance constraints, administrator interfaces, data security mandates, Node.js framework constraints, and deployment packaging requirements.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Node.js engine, the front-end frameworks, the database adapters, and the network connection matrix must behave during standard operation and under heavy enterprise transaction load.

### 2.1 Hyperledger Blockchain Explorer and its environment.

The following description outlines the intended relationship between the Hyperledger Blockchain Explorer, the end-user's web browser, the distributed peer nodes, and the underlying relational databases:

* Web requests flow from the client browser into the backend routing layer. The architecture dictates that the development team implement a Node JS web server using Express to serve these requests efficiently.
* The system must communicate seamlessly with persistent storage. The architecture requires that the engineering team implement a persistence store using Postgres, moving away from volatile in-memory storage to ensure historical block data is always queryable. Additionally, they must add the `use fabric-db` directive in the mysql schema creation scripts for teams opting for MySQL databases.
* To support massive enterprise rollouts with compartmentalized data, the architecture must support robust containerization. The framework must utilize a specific Dockerfile to start the blockchain explorer and make it as part of the fabric network setup.
* The internal networking engine must constantly evaluate the status of the blockchain. The system must implement robust abstraction by conducting an analysis and implementation of an Abstraction Layer for Different SDKs - Part 1, ensuring the backend can talk to various underlying network architectures.

The main inputs to the Explorer come from continuous block creation events, administrators configuring network profiles, and users querying specific transaction IDs. It is the job of the system's execution engine to continuously analyze these inputs, manage concurrent WebSockets, render the correct visual statistics, and deliver the compiled web pages back to the requesting client efficiently.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the explorer framework:

**Front-End User Interface and Visualization**
a. The Hyperledger Blockchain Explorer shall provide an industry-leading, highly expressive dashboard. The system must implement the front end using Bootstrap version 3.3, Jade templates 1.11.0, and Angular JS version 2 to provide a responsive, single-page application experience.
b. The system must support advanced developer and network operator data visualization. The UI must definitively avoid hardcoding configurations; currently, the list of channels is hardcoded, which must be remediated so the channel name needs to be passed to the backend to dynamically retrieve transactions.

c. Real-time telemetry is a mandatory requirement. The architecture must implement live statistics using Postgres and WebSockets, broadcasting new blocks and transaction throughput to connected clients without requiring manual page refreshes.
d. UI styling must be optimized. The build pipeline must execute a cleanup pass to remove duplicate `reset.css` files, ensuring minimal payload sizes for the client browser. Furthermore, the UI must definitively resolve the bug where users state "I cannot see items in hyperledger explorer" due to rendering or data-binding failures.

**Backend Data Ingestion and Chaincode Invocation**
e. The system shall establish a deeply integrated transaction listening architecture. The backend must properly interface with Blockchain implementation security, ensuring that it securely authenticates with the peer nodes before attempting to pull ledger data.
f. Transaction logic must be absolutely mathematically sound. A critical bug currently exists in the `java-chaincode` environment: in Chaincode-to-Chaincode invocation, the main transaction becomes successful even if the second chaincode invocation fails. This must be remediated at the SDK integration level to ensure atomic transaction integrity.
g. Security layers must be streamlined. The architecture team must evaluate if the Certificate Authority (CA) is strictly required for read-only querying. They must modify the backend to remove requiring `usercontext` if the CA should not be needed, simplifying the configuration overhead for basic block viewing.

**Network Orchestration and Docker Integration**
h. The platform must provide robust container lifecycle management. Administrators must have the capability to deploy the explorer instantly. The system must ensure that the current version of the blockchain explorer works with 1.0.2 images flawlessly.

i. Cryptographic material generation must be modernized. The system must remove the dependency on using the crypto-artifacts stored statically in the git repository and actively try to generate them dynamically using the `cryptogen` utility during the container bootstrap phase.
j. Repository cleanliness must be maintained to avoid confusing operators. The infrastructure team must remove the `fabric-docker-compose-svt/release` directory, as it contains outdated or conflicting orchestration scripts.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, data security policies, and the NodeJS architectural requirements necessary for a global cloud deployment.

### 3.1 Reliability of the framework

Reliability of the Node.js application layer, the database connections, and the resulting JSON payloads has a critical priority. The system must guarantee operational stability and security against misconfigurations and network partitions.

As a network-facing application, the system will be subject to strict cryptographic validation. The architecture must operate flawlessly regarding certificate lifecycle management. It must ensure that if peer sign certs expire, the system immediately throws a warning or error, resolving the dangerous state where a new block signature continues without warning or error despite an expired certificate. Furthermore, the system must not fail whilst generating crypto keys during the startup sequence, requiring robust error handling around the `cryptogen` binary.

Network communication mechanisms must be foolproof. The system must handle gRPC transport errors gracefully. Currently, users are getting an error while trying to connect from the REST API: `"Error": "rpc error: code = 14 desc = grpc: RPC failed fast due to transport failure"`. The backend must implement retry logic and proper backoff strategies to survive transient network drops. Additionally, the system must resolve instances where it returns `Error: Got unexpected status: SERVICE_UNAVAILABLE`, ensuring the Express server provides actionable diagnostic data rather than opaque HTTP errors.

Network topology awareness must be mathematically accurate. The architecture must ensure the Explorer can recognize all active peers accurately. Currently, the Explorer can recognize only 2 peers (when it should recognize 4 peers) and only displays one peer in the peer list. This bug must be resolved to provide an accurate network map.

### 3.2 Information volume and database performance

The system must be engineered to manage massive datasets consisting of millions of transactions, blocks, and state changes.

To support high-throughput blockchain networks, the database adapter must be aggressively optimized. The implementation of the persistence store using Postgres is specifically to handle the massive volume of transactional data that would otherwise overwhelm an in-memory or document-based store. The schema creation must include proper indexing on transaction IDs and block numbers to prevent the database from locking under the load of thousands of concurrent querying users.

When presenting long-running tasks, such as initial block synchronization, the UI must not leave the user in the dark. The WebSockets implementation must push synchronization status to the front-end so that administrators know the database is still catching up to the ledger height.

### 3.3 Developer and Administrator interface

The community of blockchain administrators, smart contract developers, and network architects requires extensive documentation and logical, predictable configuration interfaces.

Administrative configurations must be simplified. The system must simplify the `config.json` configuration in the current version, providing sensible defaults so that operators are not forced to write hundreds of lines of JSON just to connect to a local test network.

Documentation is a critical developer interface. The documentation team must provide explicitly clear instructions for porting the explorer to v1.0 of Fabric, updating the historical context that the current code was originally designed for v0.6. Furthermore, the documentation must clearly explain the modifications required in network config to connect it to any fabric network, specifically ensuring the Explorer Setting is working for Different Networks (Not just the Test Network).

The README files require extensive auditing. The team must fix the ReadMe HL Explorer documentation bug regarding directory structure and the ReadMe HL Explorer documentation bug regarding system Requirements. Additionally, installation commands must be precise: the install instructions in the readme need `sudo` added to prevent permission denied errors during global NPM installations. Finally, the character ` is put in a wrong position in the capture Architecture Deep Dive section 2.11 of the fabric doc, which must be corrected for readability.

### 3.4 User characteristics

The intended users of the Hyperledger Blockchain Explorer span from highly technical Go/Java software engineers building custom chaincode to non-technical business stakeholders verifying transaction finality on a consortium ledger.

Because the platform will be deployed globally, its interface reliability must be flawless. They require a dashboard that abstracts away the massive complexity of gRPC streams and cryptographic handshakes. The operators require clear, documented steps to setup a cluster on hyperledger v1, so that they can deploy the monitoring tool alongside their infrastructure reliably.

### 3.5 Programming language and architectural constraints

The primary programming language utilized for the underlying execution engine of the Explorer platform is JavaScript/TypeScript, running on the Node.js runtime. This mandates strict adherence to asynchronous programming paradigms, promise management, and robust relational database abstractions.

The deployment and packaging architecture must be meticulously configured to prevent upgrade failures. The system must explicitly define its runtime support; currently, node 4.x is explicitly allowed, but the `package.json` needs to be updated to ensure this is supported systematically. Furthermore, the build team must modify the package name in the `package.json` file to align with the official Hyperledger nomenclature.

The system must also account for enterprise code provenance. The engineering team is mandated to review DTCC comments and meticulously clean-up the legacy OneChain.com explorer code base that was donated, ensuring that all proprietary artifacts and branding are removed prior to the official v1.0 release.

### 3.6 Process requirements

As an enterprise-grade open-source product housed under the Linux Foundation, rigorous organizational testing, packaging, and compliance processes must be fulfilled. The product's value proposition relies entirely on its ability to maintain legal compliance, accurate versioning, and transparent communication with its global community of contributors.

The release engineering team must implement strict license headers. The pipeline must systematically add license headers to all source files in the BE (Blockchain Explorer) codebase. Furthermore, to establish clear governance, the project managers must create the initial `MAINTAINERS.rst` file to formally recognize the core contributors.

Strategic release management is critical. The team must prepare the Blockchain Explorer Upgrade recommendations document to guide users migrating from legacy architectures. Most importantly, the final milestone requires the team to formally Release the Blockchain Explorer Compatible with Fabric v 1.0 to the TSC and Provide a Demo. Only upon TSC Approval will the team officially Publish Blockchain Explorer 0.3 to the HL Open Source Community. Every action—from the extraction of localized resource packs to the compilation of the generic module loader—must be immutably tested, ensuring that the platform meets the strict regulatory and operational requirements of modern enterprise blockchain deployments.