# Spring XD

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Spring XD and its environment.
* 2.2 Product functions: The Pipes and Filters Architecture.


* 3. Other considerations.


* 3.1 High-Throughput Ingestion and Reactor I/O
* 3.2 Distributed Message Bus and Channel Registries
* 3.3 Real-Time Analytics and Metric Repositories
* 3.4 Big Data Export and HDFS Integration
* 3.5 Cloud Deployment and Operational Observability
* 3.6 Process Requirements and Build Toolchain



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of the **Spring XD** (eXtreme Data) platform. Engineered from the ground up to address the profound complexities of modern data infrastructure, this system provides a unified, distributed, and highly extensible framework that makes it easy to solve common big data problems such as massive-scale data ingestion, export, real-time analytics, and complex batch workflow orchestration.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Spring XD*, and will be referred to as the framework or "the system" in the rest of this document.

Currently, enterprise organizations attempting to build big data pipelines are forced to stitch together a highly fragmented ecosystem of disparate tools (e.g., Flume for log ingestion, Hadoop/HDFS for storage, Storm for real-time analytics, and Oozie for batch processing). This results in brittle architectures, steep learning curves, and massive operational overhead. Spring XD aims to completely abstract this "plumbing." By unifying the proven capabilities of the broader Spring portfolio—specifically Spring Integration, Spring Batch, Spring Data, and Reactor—Spring XD establishes a cohesive, domain-specific programming model for big data.

The high-level goals of this initial platform instantiation are:
a. To operationalize the prototype Distributed Integration Runtime (DIRT) into a robust, multi-node architecture capable of deploying application contexts seamlessly across a cluster of distributed containers.
b. To establish an uncompromising, high-throughput data ingestion layer leveraging Project Reactor, providing non-blocking, asynchronous network receivers for TCP, HTTP, and WebSocket protocols.
c. To architect a pluggable Channel Registry that acts as the distributed message bus connecting distinct processing modules, backed by robust, thread-safe in-memory data grids like Redis.
d. To deliver native real-time analytics capabilities, empowering developers to inject Field-Value Counters, Simple/Rich Gauges, and Message Counters directly into the data streams without writing map-reduce code.
e. To ensure frictionless integration with Hadoop, providing highly optimized HDFS ItemWriters and Sinks that natively support compression and popular big data serialization formats.
f. To provide an intuitive, text-based Domain Specific Language (DSL) that allows developers and data scientists to construct complex pipes-and-filters processing streams linearly.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions clarify the complex distributed systems terminology and architectural concepts required for the framework's implementation:

* *DIRT* – Distributed Integration Runtime. The internal prototype codename for the distributed execution engine that handles the orchestration and deployment of Spring Application Contexts across multiple physical nodes.
* *DSL* – Domain Specific Language. A text-based syntax used to define data processing streams (e.g., `http | filter | hdfs`).
* *HDFS* – Hadoop Distributed File System. The primary target for big data export and batch storage within the ecosystem.
* *Lettuce* – A scalable, thread-safe Java client for Redis based on the Netty framework. The architecture strictly mandates a switch to the Lettuce driver for Redis to handle concurrent messaging throughput safely.
* *Reactor* – A foundational reactive library for building non-blocking, asynchronous applications on the JVM based on the Reactive Streams specification.
* *Tap* – An Enterprise Integration Pattern (EIP) representing a non-destructive wiretap. It allows developers to "tap" into an existing data stream to siphon off a copy of the data for secondary processing (like real-time analytics) without disrupting the primary flow.
* *Tuple* – The fundamental data structure of Spring XD streams. It is a strictly typed, schema-aware Map representing a single unit of data flowing through the system.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the DIRT module architecture, the pipes-and-filters DSL, and the concept of Sources, Processors, and Sinks. Section 3 covers critical non-functional and deep architectural considerations, including Reactor-based I/O, Redis message bus mechanics, cloud deployment topologies (EC2/EMR), and the Gradle-based continuous integration pipeline.

---

## 2. Requirements description.

### 2.1 Spring XD and its environment.

The following description outlines the intended relationship between the Spring XD framework, its internal distributed runtime, external message brokers, and the target Big Data clusters.

Spring XD operates using a strict separation of concerns between its Admin and Container nodes.

* **The Admin Node:** Responsible for receiving DSL stream definitions via REST APIs, parsing them, and determining how to deploy the requested modules.
* **The Container Nodes (DIRT):** The worker JVMs that host the actual execution modules. The architecture requires a DIRT Runtime that deploys an application context across multiple nodes using Redis as the central coordination and metadata store.
* **The Transport Layer:** As data passes from a Source module (e.g., HTTP) in Container A to a Sink module (e.g., HDFS) in Container B, it traverses the network via a `Channel Registry`. The system must add general integration capability to the runtime nodes to abstract the underlying transport protocol.

The inputs to Spring XD are high-velocity data streams (logs, tweets, HTTP payloads) and batch jobs. The execution engine must continuously analyze these inputs, execute the stream processing graph asynchronously, maintain fault tolerance, and deliver the transformed data to the target analytical databases or Hadoop clusters.

### 2.2 Product functions: The Pipes and Filters Architecture.

The core computational functionalities of the Spring XD framework are categorized by the Enterprise Integration Patterns they enforce:

**Module Abstractions and Stream DSL**

* **Module Foundations:** Every functional component in Spring XD is a "Module". The engineering team must create strict Module base abstractions so that developers can package their custom Spring Integration or Spring Batch contexts into reusable XD components.
* **Pipes and Filters:** The fundamental architecture of data flow relies on the Pipes and Filters integration pattern. The system must create a dedicated pipes and filters DSL for ingestion. The architecture team must comprehensively design and document the desired high-level DSL for configuring data processing in XD, ensuring the syntax is logical, parseable, and extensible.
* **Parameterization:** Modules cannot be static; they require dynamic configuration at runtime. The framework must support parameterizable streams (e.g., passing specific port numbers or file paths into the DSL string) and ensure properties like `xd.stream.name` are injected via the `StreamPlugin` into the module's execution context.

**Sources, Sinks, and Wiretaps**

* **Sources:** A Source module originates data into the stream. The framework must implement a comprehensive suite of out-of-the-box sources, including a basic file source module, a tail file channel adapter (mimicking `tail -f`), and a native Twitter search source module for social media ingestion. For enterprise systems, a Gemfire CQ (Continuous Query) module for ingestion must be implemented.
* **Sinks:** A Sink module terminates a stream, writing the data to an external system. The architecture must explicitly add file sink modules alongside complex HDFS sinks.
* **Taps:** To support parallel processing architectures, the system must add tap support to DIRT. Taps must also support external observation, specifically requiring the implementation of WebSocket based taps so UI dashboards can push live data visualizations to browsers.

---

## 3. Other considerations.

### 3.1 High-Throughput Ingestion and Reactor I/O

Traditional thread-per-connection network servers fail under the massive concurrency loads required by Big Data firehoses. Spring XD addresses this by abandoning blocking I/O in favor of Project Reactor.

* **Reactor Receivers:** The ingestion layer must be built upon Reactor's asynchronous, event-driven engine (backed by the LMAX Disruptor RingBuffer pattern). The engineering team must execute a basic implementation of a Reactor-based TCP server, followed by a Reactor-based HTTP ingestion module, and a Reactor-based WebSocket ingestion module. These modules will allow a single JVM to sustain tens of thousands of concurrent connections with minimal memory overhead.
* **Syslog Ingestion:** IT infrastructure generates massive log volumes via the Syslog protocol. The architecture mandates the creation of native Syslog Ingestion modules, including generating the necessary `syslog.xml` file for the module registry and ensuring a basic performance test for syslog ingestion is established in the CI pipeline to guarantee throughput.

### 3.2 Distributed Message Bus and Channel Registries

In a multi-node DIRT architecture, when a stream is deployed, its constituent modules may land on completely different physical servers. The abstraction that bridges them is the `ChannelRegistry`.

* **Registry Abstraction:** The team must create a base Channel Registry abstraction.
* **Local vs. Distributed:** For development and single-node testing, the system must implement a `LocalChannelRegistry` utilizing in-memory queues. For production, it must utilize a `RedisChannelRegistry` acting as the distributed message broker.
* **Redis Optimization:** To ensure the framework does not bottleneck on Redis operations, the architecture mandates moving Redis Queue Channel Adapters into the broader `spring-integration-redis` project, pooling the engineering effort. Furthermore, the system must switch to use the Lettuce driver for Redis, replacing legacy drivers, because Lettuce provides thread-safe, non-blocking asynchronous connections critical for stream throughput.

### 3.3 Real-Time Analytics and Metric Repositories

Big data architectures require immediate, actionable intelligence. Spring XD natively computes analytics concurrently with data transport.

* **Counters and Gauges:** The framework must provide native analytics modules. Developers must create a simple counter service and a dedicated counter module. To track value distributions, the system requires the creation of a simple gauge service, a rich gauge service (calculating moving averages and standard deviations), and specialized field-value counters capable of counting occurrences of specific JSON/Tuple properties.
* **Repository Abstraction:** Analytics data must be queryable. The architecture specifies that Metric repositories should support the standard Spring Data `CrudRepository` interface, allowing standardized REST export. Furthermore, Redis-based repositories should use a formalized `NamingStrategy` class to calculate the name of the key to use for persistence safely, and explicitly remove the expiry of keys in Redis-based repositories to prevent inadvertent data loss of historical metrics.
* **Integration Activation:** The underlying mechanism for these metrics relies on Spring Integration. The team must implement an SI `ServiceActivator` for an XD Metrics backed Field Value Counter and an XD Metrics backed Message Counter, hooking directly into the message channels.

### 3.4 Big Data Export and HDFS Integration

The ultimate destination for the vast majority of ingested data is the Hadoop Distributed File System (HDFS). This transition from continuous streams to immutable file blocks requires sophisticated buffering and formatting.

* **HDFS Orchestration:** The framework requires an advanced Spring Integration (SI) Outbound HDFS Channel Adapter. At the lowest level, this relies on creating HDFS Core writing helper classes and a highly robust HDFS `ItemWriter` (borrowed and adapted from Spring Batch).
* **Data Compression and Formatting:** Raw text consumes exorbitant disk space on HDFS. The HDFS writing features must natively support compression codecs (Snappy, GZIP) and popular serialization formats (like SequenceFiles or Avro) before committing blocks to the NameNode.

### 3.5 Cloud Deployment and Operational Observability

Enterprise big data workloads must operate reliably within elastic cloud environments and be fully transparent to operations teams.

* **Cloud Orchestration:** The deployment team must document and execute the architectural design for deploying XD on Amazon EC2. Furthermore, because Spring XD works hand-in-hand with Hadoop, the system must explicitly support capabilities to deploy against Amazon EMR (Elastic MapReduce) clusters seamlessly.
* **JMX Monitoring:** Distributed systems are opaque without strong telemetry. To monitor container health, thread counts, and memory, the system must implement a Jolokia-based aggregator for cluster monitoring. Jolokia acts as a JMX-HTTP bridge, allowing external operational dashboards to query JMX MBeans via standardized REST/JSON payloads without grappling with complex RMI firewall ports.

### 3.6 Process Requirements and Build Toolchain

As an enterprise-grade framework intended for vast adoption, rigorous organizational build processes, test isolation, and dependency management must be established.

* **Build Automation:** The build infrastructure must transition from legacy tools to a Gradle-based multi-project build structure to handle the immense complexity of Spring XD's submodule graph. The DevOps engineers must refine the scripts because currently `build.gradle` doesn't handle a small handful of libraries correctly. Ultimately, the build script must create an executable server as an artifact (e.g., a `.zip` or `.tar.gz` with bootstrap shell scripts).
* **Continuous Integration:** A dedicated effort is required to create the CI process for the XD build.
* **Test Isolation and Feedback:** Distributed system tests are notoriously flaky if external dependencies (like Redis) are unavailable. The QA architecture mandates adding a JUnit `@Rule` so tests fail fast with clear messaging if Redis is not available on the CI agent, preventing the build from hanging indefinitely waiting for network timeouts.

Only through rigorous adherence to these reactive I/O paradigms, distributed registry abstractions, and deep cloud mechanics can Spring XD successfully provide a flawless, secure, and highly performant foundation for enterprise big data pipelines.