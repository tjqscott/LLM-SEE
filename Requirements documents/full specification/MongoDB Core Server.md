# MongoDB Core Server

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 MongoDB Core Server and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability, Security, and Fault Tolerance
* 3.2 Information volume and Memory Optimization
* 3.3 Developer and Database Administrator interface
* 3.4 User characteristics
* 3.5 Architectural constraints and deployment
* 3.6 Process requirements and Testing Matrices



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of a highly scalable, distributed document database. This system is engineered from the ground up to provide a schema-less, highly available, and horizontally scalable backend for modern web and enterprise applications. By moving away from rigid relational tables and embracing rich, hierarchical documents, the platform will empower developers to iterate rapidly while handling massive datasets.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *MongoDB Core Server* (with enterprise capabilities designated for the MongoDB Enterprise Server edition), and will be referred to as MongoDB, the Core Server, or "the system" in the rest of this document.

The primary purpose of the MongoDB Core Server is to act as the foundational database execution engine. Modern applications struggle with the object-relational impedance mismatch; developers write code using rich, nested objects in memory, but are forced to flatten this data into rigid tables for database storage. MongoDB aims to solve this by natively storing data in BSON (Binary JSON), allowing for deeply nested structures, dynamic schemas, and embedded arrays.

To ensure the success of this ambitious architecture, the engineering team must first ensure a rock-solid foundation, acknowledging that currently, in the prototype branches, "something is broken" regarding fundamental stability, requiring a comprehensive stabilization phase prior to release.

The high-level goals of this new platform instantiation are:
a. To radically democratize horizontal scaling by engineering a native "Sharding" architecture. The system must seamlessly distribute data across commodity hardware, specifically requiring intelligent query routers (`mongos`) that ensure `mongod` forwards writes to the correct server based on partition boundaries.
b. To establish a highly resilient, self-healing network topology utilizing Replication Pairs. The architecture must guarantee that a slave node should be able to replicate from a repl pair cleanly, providing automatic failover and high availability.
c. To provide an uncompromising, highly optimized query execution engine that fully supports advanced indexing. The system must automatically add an index on `_id` upon collection creation to guarantee primary key enforcement, and implement robust unique indexes.
d. To ensure flawless integration with dynamic execution environments, the platform will embed a JavaScript engine. However, strict computational boundaries must be enforced, including the implementation of infinite loop protection for `$where` clauses and `dbEval` commands to prevent single queries from locking the database.
e. To deliver an extensible suite of operational utilities, ensuring administrators have access to native MongoDB tools (like `mongodump` and `mongorestore`) for hot backups and data migration.
f. To provide granular, enterprise-grade resource control. The system must expose commands allowing administrators to query the total allocated file space, while internally ensuring that the stack size per thread isn't too big, preventing memory exhaustion under high connection concurrency.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the database server's implementation:

* *BSON* – Binary JSON. The binary-encoded serialization of JSON-like documents used by MongoDB for storage and network transfer.
* *Grid* – The internal namespace and routing architecture for the sharded cluster. The system must optimize internal placement logic, specifically making `Grid::pickServerForNewDB()` smarter to evenly distribute initial database payloads.
* *Mongod* – The primary daemon process for the MongoDB system. It handles data requests, manages data access, and performs background management operations.
* *Mongos* – The routing service for MongoDB shard configurations. It processes queries from the application layer and determines the location of the data in the sharded cluster to route the operations appropriately.
* *Replica Pair* – The predecessor architecture to Replica Sets, providing two-node replication with an arbiter. The system relies heavily on automated scripts to test repl pair negotiations and failovers.
* *Shard Key* – The indexed field or fields that MongoDB uses to distribute documents across shards. The system must support advanced partition models, explicitly supporting a Shard Key compound key for high-cardinality distribution.
* *SpiderMonkey* – The embedded JavaScript engine (developed by Mozilla) utilized by MongoDB to execute server-side JavaScript for MapReduce and `$where` queries.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the indexing structures, the sharding algorithms, BSON document querying, and cursor iteration. Section 3 mentions other necessary considerations, including strict memory constraints, replica fault tolerance, operating system interactions, the comprehensive JavaScript testing matrix, and deployment architectures.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core C++ engine, the query optimizer, the balancing algorithms, and the replication oplog must behave during standard operation and under heavy enterprise load.

### 2.1 MongoDB Core Server and its environment.

The following description outlines the intended relationship between the MongoDB Core Server, the host operating system, the client drivers, and the distributed cluster topology:

* Client applications communicate with the database via binary drivers over TCP/IP. The database operates using a thread-per-connection model. To prevent Out-Of-Memory (OOM) errors on high-traffic servers, the architecture must actively assure the stack size per thread isn't too big.
* In a distributed environment, clients connect to a `mongos` router rather than a `mongod` directly. The `mongos` router caches the cluster metadata from the Config Servers. To prevent stale metadata from corrupting data reads, the system must robustly check for a config change mid-cursor iteration on another server.
* When managing distributed data structures, the internal cluster configurations must be strictly typed. A critical defect must be resolved where `config.shard` docs erroneously have elements of type `-1`, which corrupts cluster routing maps.
* The storage engine relies heavily on the operating system's virtual memory manager and Memory Mapped Files. While this provides high performance, it requires graceful handling of environmental limitations, explicitly demanding the graceful handling of "Disk Full" conditions to prevent database corruption.

The main inputs to MongoDB come from client drivers submitting BSON payloads, query operators, and administrative commands. It is the job of the system's execution engine to continuously analyze these inputs, execute query plans using B-Tree indexes, manage concurrent locking, and deliver the matched BSON documents via batch cursors.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the database engine:

**Query Execution, Cursors, and BSON Manipulation**
a. MongoDB shall provide an industry-leading, highly expressive query engine capable of querying deeply nested documents. The dot-notation parser must be flawless; currently, a `find` on `x.y.z` does not seem to work for complicated objects, and the BSON traversal logic must be rewritten to support infinitely nested arrays and sub-documents.
b. The query language must support complex logical exclusions. The engine must explicitly support the negated `$in` operator (i.e., `$nin`) natively within the C++ matcher.

c. Cursor management must be strictly memory-safe and mathematically accurate. A critical defect must be resolved where cursors can return the same object twice during concurrent update operations; the engine must implement document deduplication based on `_id`.
d. Pagination must interact seamlessly with count aggregations. The `dbcursor.count()` method should update based on `limit()` and `skip()` modifiers dynamically, providing accurate results for paginated user interfaces. Furthermore, the network response protocol needs to explicitly set the `#returned` variable in the query result header so clients know exactly how many documents were batched.
e. A highly requested feature must be designed: the system must implement index-based constraints and field "mutators", allowing for database-level data validation and automatic field transformations upon insert.

**Indexing and Performance Optimization**
f. The system shall establish a highly performant B-Tree indexing architecture. To reduce developer friction, the system should get rid of mandatory index names, auto-generating them based on the index key pattern if the user does not provide one.
g. Data integrity rules rely heavily on indexes. The architecture must guarantee that unique index behavior is consistent across single-node and sharded environments, fixing existing inconsistencies.

h. Index creation must be reliable. During cross-node data transfers, the cloning protocol (`cloner.cpp`) must be bulletproof. Bugs where `clonecollection.js` sometimes fails to clone the index as expected must be resolved to ensure secondary nodes contain the exact same query optimizations as primary nodes.

**Sharding and Horizontal Scalability**
i. The core mechanism for scaling write throughput is "Sharding". To ensure data is distributed evenly, the system requires a `mongos` router. The internal namespace must be organized; the architecture team must put all sharding commands in a dedicated namespace for clarity.
j. Data is distributed based on a Shard Key. The system must enforce a strict `ensureIndex` on the ShardKey before a collection can be sharded, guaranteeing that chunk routing can execute index scans.
k. As data grows, "Chunks" must be split and migrated. The balancing process must make a mid-data split move if needed to maintain cluster equilibrium. Furthermore, the system must explicitly move the shard after a split completes.
l. The splitting algorithm relies on calculating the median of a chunk's data size. The system must check the return of the median calculation strictly—it must not allow splitting an empty shard, which would result in infinite looping or division by zero errors.

m. The system must provide global aggregation capabilities. The architecture must seamlessly execute a `count()` for sharded collections, fanning the query out to all relevant shards and merging the results at the `mongos` layer.
n. Multi-router topology must be supported. The synchronization protocol must make resync work correctly across multiple `mongos` instances, ensuring all routers have the same config metadata.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics under massive data volume, strict reliability and replica fault-tolerance mandates, JavaScript sandboxing, and the exhaustive test matrices required for database CI/CD.

### 3.1 Reliability, Security, and Fault Tolerance

Reliability of the C++ database layer, the network connections, and the resulting BSON data artifacts has a critical priority. The system must guarantee operational stability, high availability, and secure execution of user-defined scripts.

The high-availability architecture relies on Replica Pairs (and future Replica Sets). The network negotiation protocol between these nodes must be absolute. In testing, the `pair3.js` test fails due to one server remaining in a negotiating (`-1`) state instead of moving to a "can't arb" (`-3`) state; the state machine must be hardened to ensure split-brain scenarios resolve cleanly.

Failover transitions must be instantaneous. A critical defect identified in the `pair1.js` test indicates that the left node never becomes master after the right node gets a `SIGKILL`. The heartbeat and election algorithms must be completely rewritten to guarantee a new master is elected within seconds. Furthermore, the recovery process must be flawless; the system absolutely needs to ensure consistency on repl pair recovery, ensuring the operation log (oplog) is applied identically to prevent data divergence.

Security requires strict computational sandboxing. MongoDB allows developers to execute JavaScript on the server using `$where` clauses. However, malicious or poorly written scripts can crash the database. The engineering team must implement infinite loop protection in SpiderMonkey specifically to safeguard `$where` and `dbEval` execution. Additionally, the system must fix the segmentation fault/crash when calling `tojson(x)` on complex objects in the interactive shell.

### 3.2 Information volume and Memory Optimization

The database must be engineered to manage unprecedented datasets consisting of billions of documents and terabytes of throughput.

The storage engine relies on flushing memory-mapped files to disk. To provide durability controls to the application layer, the system must implement a requested feature: "Flush this record(s) to disk", allowing applications to force a physical write (fsync) for critical transactions rather than waiting for the background flushing thread.

Data validation at the network boundary must be strict. When client applications submit massive or malformed payloads, the system must reject them gracefully. A defect in `clientTest` where it fails to clear a collection (complaining about "Invalid BSONObj spec size") must be resolved by enforcing absolute BSON size limits (e.g., 16MB) at the parser level.

### 3.3 Developer and Database Administrator interface

The community of database administrators and software engineers requires extensive documentation, reliable tooling, and highly predictable configuration interfaces.

Administrative configurations must be dynamic but file-driven. The system must implement robust file configuration (e.g., `mongod.conf` YAML/INI files) to replace massive command-line argument strings. To support complex server topologies, the daemon must add an option to bind to different interfaces/IPs, rather than defaulting to `0.0.0.0`, to secure the database behind specific private networks.

Diagnostic visibility is a core requirement. The `inprog` command must be updated to provide better diagnostics, exposing the exact lock states and execution times of running queries. For general infrastructure monitoring, administrators require a Server Info Command to output exact binary versions, host OS specs, and uptime.

### 3.4 User characteristics

The intended users of MongoDB Core Server are highly technical backend software engineers, Site Reliability Engineers (SREs), and Database Administrators (DBAs). They are intimately familiar with JSON/BSON structures, network latency, and distributed systems. They require an interface that is extremely dense with audit data and highly responsive. When scaling a cluster, they demand absolute determinism; a `mongos` must never drop a write, and a secondary node must never fall infinitely behind a primary.

### 3.5 Architectural constraints and deployment

The primary programming language utilized for the underlying execution engine of the MongoDB platform is C++. This mandates strict adherence to manual memory management, pointer safety, and high-performance multithreading architectures.

A severe memory assertion must be fixed: the `pair1.js` test fails with a `c.get()` assertion in `cloner.cpp`, indicating a dangling pointer or concurrent modification during collection cloning. To ensure developers can safely interact with the C++ core and the test matrix, the build pipeline must be highly optimized.

### 3.6 Process requirements and Testing Matrices

As an enterprise-grade database product, rigorous organizational testing, versioning, and performance benchmarking processes must be fulfilled. The product's value proposition relies entirely on its ability to prove its data integrity.

The continuous integration (CI) pipeline must be fast and comprehensive. The infrastructure team must make replication tests faster to decrease feedback loops for C++ developers.

The JavaScript testing matrix is currently exhibiting severe instability that must be triaged immediately prior to release:

* The system must resolve the intermittent issue where the final write in the `clonecollection.js` test did not clone to the secondary.
* The `repl7.js` test times out waiting for all databases to be cloned; the underlying replication throughput must be increased to pass this threshold.
* A fundamental communication failure during the `repl1.js` test must be diagnosed at the TCP socket layer.
* The `repl6.js` test fails on a basic `count` validation, indicating potential oplog application latency.
* The `pair4.js` script fails specifically during the `n:2` node topology test.
* A new `mongod` instance fails to bind to the assigned port in the `replacePeer1.js` test, requiring better socket teardown handling (e.g., `SO_REUSEADDR`).

Finally, the engineering team must establish a culture of performance tracking. The continuous integration pipeline must automatically post benchmark data to a web app upon every successful build, allowing the leadership team to track throughput regressions across commits visually over time. Only through rigorous adherence to these testing matrices, process guidelines, and strict C++ architectural constraints can MongoDB successfully deploy its distributed database to the global enterprise community.