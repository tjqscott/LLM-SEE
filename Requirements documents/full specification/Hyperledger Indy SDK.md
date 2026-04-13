# Hyperledger Indy SDK

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Hyperledger Indy SDK and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability, Logging, and Error Handling
* 3.2 Information volume and Cryptographic overhead
* 3.3 Developer interfaces and CLI Tools
* 3.4 User characteristics
* 3.5 Programming language and architectural constraints
* 3.6 Process requirements and Testing Matrices



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of the Hyperledger Indy Software Development Kit (SDK). This system is engineered from the ground up to provide a distributed-ledger-based foundation for self-sovereign identity (SSI). It aims to provide a robust software ecosystem for private, secure, and powerful identity management, empowering developers to build clients that interact seamlessly with the Indy distributed ledger.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named the *Hyperledger Indy SDK*, and will be referred to as the Indy SDK or "the system" in the rest of this document.

The primary purpose of the Hyperledger Indy SDK is to serve as the foundational bridge between client applications (such as digital wallets and identity agents) and the decentralized Hyperledger Indy Node network. Currently, developers face an immense barrier to entry when interacting with blockchain-based identity protocols; they are required to manually construct complex cryptographic proofs, manage raw socket connections, and securely handle private key material in memory. The Indy SDK aims to abstract this complexity entirely.

The major artifact of the SDK will be a highly optimized, cross-platform C-callable library. Surrounding this core engine, the project will simultaneously deliver convenience wrappers for various modern programming languages (specifically Python and iOS/Objective-C/Swift) alongside an interactive Indy Command Line Interface (CLI) tool.

The high-level goals of this new platform instantiation are:
a. To radically standardize identity nomenclature across the ecosystem by mandating that the SDK and its clients use consistent terminology for Agent and Wallets per the Sovrin Provisional Trust Framework V2 whitepaper.
b. To establish a highly secure, locally encrypted storage enclave by implementing a robust Wallet API that includes explicit requirements to add security to the wallet, safeguarding private keys and Decentralized Identifiers (DIDs) at rest.
c. To provide an uncompromising, native development experience for Apple ecosystems by explicitly engineering MacOS support, requiring the build systems to compile the core `libsovrin` (the legacy name transitioning to `libindy`) library specifically for MacOS architectures.
d. To ensure flawless interoperability between the core cryptographic engine and privacy-preserving credential formats, specifically mandating strict Anoncreds API interoperability with the core C-callable library to support zero-knowledge proofs natively.
e. To deliver an unassailable test-driven development pipeline that prevents technical debt from accumulating, requiring extensive integration tests across all wrapper languages categorized by low, medium, and high-level cases.
f. To provide granular, enterprise-grade peer-to-peer communication by implementing a dedicated Agent API utilizing the PairwiseCurveCP protocol for secure, encrypted, off-ledger messaging.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the identity SDK's implementation:

* *Agent* – A software representative that acts on behalf of an identity owner to interact with other agents and the ledger. (Terminology governed by the Sovrin Provisional Trust Framework V2).
* *Anoncreds* – Anonymous Credentials. A privacy-preserving credential format that allows users to present verifiable claims using Zero-Knowledge Proofs (ZKPs) without revealing correlatable identifiers.
* *DID* – Decentralized Identifier. A globally unique identifier that does not require a centralized registration authority. The SDK will feature a dedicated DID API.
* *PairwiseCurveCP* – A secure, encrypted, reliable transport protocol based on elliptic curve cryptography, used by the SDK's Agent API to establish private communication channels between peers.
* *Signus* – The cryptographic signing and encryption module within the SDK. It handles the creation of key pairs, signing payloads, and verifying signatures.
* *Wallet* – A secure storage mechanism managed by the SDK, used to store link secrets, private keys, DIDs, and verifiable credentials. (Terminology governed by the Sovrin whitepaper).
* *xUnit* – A standard XML-based format for test execution reporting. The CI/CD pipelines require all test logs in xUnit format to integrate with external build dashboards.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the C-callable core library and the specific language wrappers (Python and iOS). Section 3 mentions other necessary considerations, including strict performance constraints, logging architectures, developer interfaces, the CLI tool, and rigorous testing process requirements.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core C library, the Foreign Function Interfaces (FFI), the cryptographic engines, and the high-level language wrappers must behave during standard operation.

### 2.1 Hyperledger Indy SDK and its environment.

The following description outlines the intended relationship between the Hyperledger Indy SDK, the host operating system, the client application, and the distributed ledger network:

* Client applications (written in Python, Swift, Java, etc.) invoke methods on the high-level language wrappers.
* These wrappers execute Foreign Function Interface (FFI) calls down into the core C-callable library (`libindy`/`libsovrin`).
* The core library manages all complex state, maintaining asynchronous ZMQ (ZeroMQ) socket connections to the distributed Hyperledger Indy node pool via the `Pool API`.
* The core library interacts securely with the host operating system's file system or secure enclave to manage encrypted SQLite databases representing the `Wallet`.
* The architecture must operate identically across varied deployment environments. Developers must be able to compile the core engine and its wrappers for Linux, Windows, and explicitly MacOS.

The main inputs to the SDK come from client applications requesting identity generation, credential verification, or ledger state queries. It is the job of the SDK's execution engine to continuously analyze these inputs, construct highly specific cryptographic payloads, serialize them into proper ledger transaction formats, and deliver the requests asynchronously to the network consensus pool.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the identity framework. Because the SDK is heavily driven by cross-platform parity, these requirements detail the APIs that must be implemented across the core library and its corresponding wrappers.

**Core API Definitions and Abstractions**
a. The SDK shall provide a unified **Wallet API** to manage local secrets. The architecture must explicitly add security to the wallet, utilizing modern symmetric encryption algorithms (e.g., XSalsa20/Poly1305) to encrypt the wallet payload at rest, ensuring that compromised devices do not leak private keys.
b. The SDK shall provide a comprehensive **Signus API** to abstract complex cryptographic operations. This API must handle the generation of ED25519 key pairs and support the signing and verification of arbitrary payloads without exposing the private key material to the wrapper languages.
c. The SDK shall provide a **Ledger API** to format, sign, and submit transactions (like NYM, SCHEMA, and CRED_DEF) to the Indy distributed ledger, as well as parse the cryptographic state proofs returned by the nodes.
d. The SDK shall provide an **Anoncreds API** capable of handling heavy Zero-Knowledge Proof (ZKP) mathematics. The architecture must guarantee seamless interoperability with libsovrin's core cryptographic primitives to ensure that generating a credential proof does not bottleneck the client device.

e. The SDK shall provide a **Pool API** to maintain network state, connect to validator nodes using a genesis transaction file, and manage the asynchronous routing of consensus read/write requests.
f. The SDK shall provide an **Agent API** for off-ledger communication. This must implement the PairwiseCurveCP protocol, allowing two mobile devices or servers to establish a secure, authenticated, end-to-end encrypted channel based purely on their exchange of DIDs.

**Python Wrapper Implementation**
g. The system shall provide a native Python wrapper for backend enterprise integrations. The team must complete the comprehensive Python Wrapper API definition, ensuring it feels pythonic while accurately wrapping the C-callable core.
h. The Python wrapper must fully implement the underlying core APIs, specifically exposing the Pool API, Ledger API, Agent API, Wallet API, and Signus API to Python developers.
i. To ensure developers have working reference material, the engineering team must port demo tests directly into the Python Wrapper repository, providing executable examples of complete identity workflows.
j. The Python distribution must be seamless. The infrastructure team must configure the build pipeline to generate standard Python Packages (e.g., pip/PyPI compatible wheels) containing the compiled C-library binaries for target architectures.

**iOS Wrapper Implementation**
k. The system shall provide a native iOS wrapper (Objective-C/Swift) to empower mobile edge-agents. The iOS wrapper must expose the core functionalities cleanly to mobile developers.
l. The iOS wrapper team must port demo tests to the mobile environment, ensuring that reference applications can be built immediately.
m. Specifically, the iOS wrapper must implement and provide demo tests for the Ledger API, Signus API, Anoncreds API, and Wallet API.
n. The iOS Wrapper must implement the Agent API to allow mobile devices to communicate securely via Pairwise connections with enterprise issuers.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, complex logging architectures, developer interface (CLI) requirements, and the massive testing matrices required to validate cryptographic libraries.

### 3.1 Reliability, Logging, and Error Handling

Reliability of the C-callable library and its memory management has a critical priority. Because the SDK will run on resource-constrained mobile devices and highly concurrent enterprise servers simultaneously, the core engine must prevent memory leaks and segmentation faults.

Error handling across language boundaries (FFI) is notoriously difficult. To prevent legacy accumulation and silent failures, the initial architecture must preemptively address technical debt and execute a comprehensive errors refactoring. All errors emitted by the C-library must conform to a standardized enum structure that the Python and iOS wrappers can translate into native exception types.

Visibility into the SDK's internal state is paramount for debugging. However, a hardcoded logging mechanism will clash with host applications. Therefore, Libindy should provide an API for logger configuration that can be seamlessly integrated with the host application's native logging approach (e.g., Python's `logging` module or iOS's `os_log`), allowing developers to capture SDK trace logs within their own application monitoring tools.

### 3.2 Information volume and Cryptographic overhead

The SDK must be engineered to manage the creation and verification of complex cryptographic proofs in milliseconds. Anoncreds (Anonymous Credentials) utilize heavy pairing-based cryptography. The execution of these proofs must not block the main thread of the host application. The core library must be entirely asynchronous, utilizing callback mechanisms or futures/promises across the FFI boundary so that mobile UI threads remain responsive while a Zero-Knowledge Proof is being generated.

Furthermore, the wallet storage mechanism must be optimized. As an identity owner accumulates hundreds of digital credentials, the Wallet API must execute indexed queries against the encrypted SQLite store efficiently, ensuring that parsing the wallet does not become a computational bottleneck.

### 3.3 Developer interfaces and CLI Tools

The community of identity developers, network administrators, and system integrators requires extensive documentation, predictable APIs, and powerful diagnostic tools.

The Indy Command Line Interface (CLI) is a critical developer tool for interacting with the ledger without writing a custom application. The CLI parsing engine must be highly flexible. To support advanced ledger modifications, the architecture team must introduce the special value "null" for parameters of "send" commands to explicitly signal a field removal on the ledger, distinguishing between an empty string and a deletion request.

Documentation must be treated as a first-class feature. To support Apple ecosystem developers, the team must explicitly create the `.md` file with build instructions for MacOS, detailing the necessary toolchains, dependency managers (like Homebrew), and environment variables required to compile the C-library natively on Darwin architectures.

### 3.4 User characteristics

The intended users of the Hyperledger Indy SDK span from highly technical systems engineers building the core Rust/C library to high-level Python backend developers and mobile iOS developers integrating digital wallets into existing consumer applications.

Because the SDK is a foundational library, it must abstract away the massive complexity of distributed ledgers. A Python developer should not need to understand Byzantine Fault Tolerance to query a schema, and an iOS developer should not need to understand elliptic curve cryptography to establish an Agent connection. The SDK's API surfaces must be strictly domain-driven, utilizing the terminology defined in the Sovrin Trust Framework.

### 3.5 Programming language and architectural constraints

The primary programming language utilized for the underlying core execution engine is mandated to be a systems-level language capable of compiling to a C-callable Application Binary Interface (ABI). Typically in the Indy ecosystem, this is implemented in Rust. This mandates strict adherence to memory safety, un-garbaged collected lifecycle management, and thread-safe execution contexts.

The deployment and packaging architecture for the MacOS environment must be meticulously configured. The CI/CD pipelines must support MacOS explicitly. The infrastructure team must establish MacOS Support for Continuous Delivery (CD) and Packages, ensuring that Homebrew formulas or pre-compiled dynamic libraries (`.dylib`) are generated and signed automatically upon every release.

### 3.6 Process requirements and Testing Matrices

As an enterprise-grade open-source product housed under the Linux Foundation, rigorous organizational testing, packaging, and compliance processes must be fulfilled. The product's value proposition relies entirely on its cryptographic accuracy, meaning test coverage must be exhaustive.

The continuous integration (CI) pipeline must be standardized to allow cross-platform reporting. The infrastructure team must resolve existing technical debt by ensuring all test logs across all languages are generated strictly in the xUnit format.

The QA and development teams are mandated to execute a massive matrix of integration tests, categorized by severity and complexity (High, Medium, and Low level cases):

**Core C-Library Testing Requirements**

* Execute DID API integration tests covering Low cases.
* Execute Signus API integration tests covering Medium and High level cases.
* Execute Wallet API integration testing covering High cases.
* Execute Crypto API integration testing covering Low cases.
* For MacOS support, the CI must build libsovrin for mac and explicitly run the tests on Apple hardware.

**Python Wrapper Testing Requirements**

* Implement Python Wrapper Signus API integration tests (High cases).
* Implement Python Wrapper Wallet API integration tests (High cases).
* Implement Python Wrapper Agent API integration tests (High cases).
* Implement Python Wrapper Ledger API integration tests (High cases).
* Implement Python Wrapper Pool API integration tests (High cases).

**iOS Wrapper Testing Requirements**

* Implement iOS Wrapper Signus API integration tests covering High and Medium level cases.
* Implement iOS Wrapper Ledger API integration tests covering High and Medium level cases.
* Implement iOS Wrapper Wallet API integration tests covering High and Medium level cases.
* Implement iOS Wrapper Pool API integration tests covering High and Medium level cases.
* Implement iOS Wrapper Agent API integration tests covering High and Medium level cases.
* Implement iOS Wrapper Anoncreds API integration tests, specifically separating Primary Claims integration tests (High cases) and Revocation integration tests (High cases).

Only through rigorous adherence to these testing matrices, process guidelines, and architectural constraints can the Hyperledger Indy SDK successfully provide a flawless, secure, and performant foundation for the future of global self-sovereign identity.