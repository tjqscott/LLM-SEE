# Apache Mesos

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Apache Mesos and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and compilation
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive software requirements and architectural specifications for a highly scalable, fault-tolerant system designed to manage large-scale computer clusters. This system is engineered to abstract computing resources—such as CPU, memory, and storage—away from specific physical or virtual machines, presenting them as a single, unified pool of resources to distributed applications and frameworks.

### 1.1 The Project at a Glance

The software to be produced will be officially named *Apache Mesos*, and will be referred to as Mesos in the rest of this document. It is an open-source project originally conceptualized and developed in the C++ programming language at the University of California, Berkeley.

The primary purpose of Apache Mesos is to act as a distributed systems kernel that manages computer clusters. The client development community and enterprise organizations currently utilize statically partitioned infrastructure, dedicating specific machines to specific tasks (e.g., a siloed Hadoop cluster next to a siloed web server cluster). This antiquated methodology leads to massive resource underutilization and brittle operational architectures. Mesos aims to phase out this static partitioning model by dynamically sharing cluster resources among various distributed computing frameworks.

During the initial evolutionary phases of the project architecture, there was an initiative to rename all components to be references to Firefly, though the core system remains functionally focused on distributed resource management.

The high-level goals of the new distributed system are:
a. To provide a standardized, programmatic interface that allows administrators and automated tools to programmatically query the Mesos cluster state at any given moment.
b. To increase the stability and extensibility of intra-cluster communication by forcing a switch in the communication layer to use protocol buffers instead of legacy message formats.
c. To drastically improve distributed workload observation by ensuring the master node maintains a history of executed frameworks and tasks, and subsequently shows it on the web UI.
d. To support major big-data processing paradigms by explicitly porting the Hadoop framework to the new Java API, ensuring seamless interoperability.
e. To ensure strict resource isolation guarantees by utilizing advanced containerization, specifically demanding that the LXC isolation module kills entire containers on OOM (Out of Memory) events to protect the host system.
f. To provide robust educational and onboarding materials, including a step-by-step tutorial of Mesos running two versions of Hadoop simultaneously to demonstrate multiplexing capabilities.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the cluster manager's implementation:

* *Executor* – A process launched on worker nodes (slaves) that runs the actual tasks for a framework. The system must ask executors to shutdown when a framework goes away to prevent zombie processes.
* *Framework* – A distributed application running on top of Mesos, such as Hadoop. Mesos must negotiate resources with these frameworks seamlessly.
* *JNI* – Java Native Interface. Because Mesos is built in C++, JNI bindings are used to interface with Java frameworks like Hadoop. These JNI bindings shouldn't segfault when passed invalid parameters.
* *LXC* – Linux Containers. The underlying isolation module used by the system to restrict resource usage. External tests surrounding LxcIsolation frequently encountered wrong paths that must be remediated.
* *Master* – The central control plane node that delegates resources. The master should display the cluster URL on the web UI for easy operational access.
* *Protocol Buffers* – A language-neutral, platform-neutral, extensible mechanism for serializing structured data. Both the master and slaves should be extremely defensive of badly formed protobufs to prevent network-based crashing.
* *Slave* – The worker node in the cluster that executes the containerized tasks. The slave requires the `MESOS_HOME` environment variable to be set in order to invoke `killtree` commands effectively.
* *Zookeeper / Replicated Log* – The distributed coordination service used for high availability. When the system is reading from the `beginning()` to the `ending()` of a replicated log, it must strictly have "safe" semantics to guarantee state machine consistency.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the resource allocation, web interface, and container isolation environments. Section 3 mentions other necessary considerations, including performance constraints, developer interfaces, and strict C++ programming language dependencies.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the cluster master, slaves, and isolation modules must behave.

### 2.1 Apache Mesos and its environment.

The following description outlines the intended relationship between Mesos, the physical data center hardware, and its surrounding compilation and execution environment:

* Workload execution requests flow from user-defined Frameworks (like Hadoop) to the Mesos Master.
* The Mesos Master delegates task specifications down to the Mesos Slaves, which utilize the LXC isolation module to partition CPU and memory.
* Real-time telemetry, stdout, and stderr logs flow from the executors running on the slaves back to the slave webui, which then passes representations back to the master.
* Developer contributions and compilation workflows flow through automated deployment systems, where it is required to create a build to run on `builds.apache.org`.
* End-users and testers operate in disparate environments, necessitating the creation of a downloadable VM image of Mesos on Ubuntu Linux to standardize initial evaluations.

The main inputs to Mesos come from the frameworks requesting resources and the slaves reporting available hardware capacity. It is the job of the system's allocator to continuously analyze and process these offers, generate protobuf-based negotiation messages based on them, and deliver the compiled operational directives to the distributed nodes.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the cluster management framework:

**Resource Allocation and Isolation**
a. The Mesos Framework shall provide a sophisticated, pluggable resource allocation subsystem. To ensure fairness across competing frameworks, the engineering team must implement a simple revocation policy explicitly within the `SimpleAllocator` component.
b. The system must ensure that physical node resources are not oversubscribed. The LXC isolation module currently doesn't account for queued task's resource usage, which leads to instability; the system must aggregate queued usage into its accounting metrics.

c. The Linux container isolation module must be robust during state transitions. Previously, killing frameworks from `resourcesChanged` events caused system crashes; this lifecycle handling must be stabilized to ensure safe teardowns. Furthermore, there are path problems in `lxc` that must be permanently resolved to ensure containers can consistently locate their root filesystems.
d. To prevent unbounded memory consumption, the framework must aggressively kill entire containers on OOM (Out of Memory) using the LXC isolation module, preventing a single rogue task from bringing down an entire slave node.

**Inter-Process Communication and Stability**
e. The Mesos Framework must ensure that all internal cluster communication is strongly typed and backwards-compatible. The system will switch all communication to use protocol buffers.
f. Due to the distributed nature of the system, network packets may be corrupted or intentionally malformed. Therefore, both the master and slaves should be defensive of badly formed protobufs, rejecting them gracefully without triggering a fatal process crash.
g. The system must carefully manage the lifecycle of long-running executor drivers. Engineers must eliminate a known race condition on `MesosExecutorDriver` destruction specifically for the Python bindings. Furthermore, the architecture team must deliberately remove the `failover` flag from the executor driver to simplify the state machine.

**Web User Interface and Observability**
h. The Mesos Framework shall provide a comprehensive Web UI for operational visibility. The master should display the cluster URL on the web UI to ensure administrators know exactly which logical cluster they are viewing.
i. The system shall maintain a history of executed frameworks and tasks, and persistently show it on the web UI for auditing and debugging purposes. To handle large volumes of historical data, developers must improve the tables in the Mesos Web UI to be dynamically sortable by category.
j. The framework's internal UI routing must be accurate. Previously, the slaves table in the master's index web ui page always linked to the slave web ui at port 8081 regardless of which port the slave's webui was actually operating on; this hardcoded value must be replaced with dynamic port discovery.
k. The slave webui needs to correctly display the `stdout` and `stderr` streams of local executors, and the framework must fix the slave webui representation and correctly pass this aggregated data back to the master. Furthermore, when rendering JSON data to the frontend, the system needs to escape strings properly to prevent UI rendering errors or cross-site scripting vulnerabilities.

**Framework Integration (Hadoop)**
l. The Mesos Framework must ensure seamless integration with Apache Hadoop. The team must port the Hadoop framework to the new Java API.
m. Edge cases during task commits must be handled gracefully. Previously, Hadoop executors were being forcefully killed while tasks were in a `COMMIT_PENDING` state, leading to data corruption; the state machine must recognize this pending state and await completion.
n. The system must also resolve the specific trouble starting a Hadoop datanode when utilizing the bundle version of hadoop, specifically version `hadoop-0.20.2`.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, and developer experience requirements.

### 3.1 Reliability of the framework

Reliability of the C++ core and the resulting distributed execution environment has a critical priority. The system must guarantee total operational stability, which means eliminating fatal assertions in the codebase. The team must resolve a specific `CHECK` failure in `sched.cpp:467` attempting to send a framework message to a slave where the condition `slave != UPID()` unexpectedly failed. Similarly, developers must fix the `CHECK` failure in `coordinator.cpp:39` which triggered the `Check failed: !elected` panic.

When handling security and access control, the system must be flawless. A severe bug where the Master Detector uses the wrong ACL when authentication is not required must be patched immediately to prevent unauthorized cluster manipulation.

Resource leaks are unacceptable in a long-running daemon. The system must be patched because Mesos currently leaks file descriptors to `lxc-execute`, which eventually exhausts the host OS file descriptor limits and causes the slave daemon to halt. Finally, the framework must add a timeout to external tests to prevent continuous integration builds from hanging indefinitely when subsystems deadlock.

### 3.2 Information volume and compilation

The system should be able to manage tens of thousands of nodes efficiently, and the runtime must not suffer from slow initialization or compilation failures on supported platforms. The system's deployment automation must be pristine; administrators must update deploy scripts to pass the new `--resources` parameter correctly to thousands of nodes simultaneously.

Furthermore, to handle large-scale observability, the system must implement robust executor resource monitoring and local reporting of usage stats natively within the node daemon.

During the compilation phase, the system has historically suffered from platform-specific degradation. The latest (Jun 27 2011) Mesos codebase doesn't compile on Mac OS X - Snow Leopard, and generates multiple Mac OS X Lion errors. Additionally, compilation was broken entirely on Ubuntu Lucid on the `twitter` branch. The build system must be rigorously standardized across these POSIX environments to handle the massive volume of source code. To support the Java ecosystem's volume of dependencies, the team must also generate and maintain Maven poms for Mesos.

### 3.3 Developer interface

The community expressed repeatedly that the developer interface, onboarding experience, and documentation of the system should be a major priority. The project must explicitly document semantics and state transitions in all Mesos user-pluggable interfaces so that third-party framework authors can reliably build on top of the kernel.

The educational onboarding process must be frictionless. The user wants to have high-quality, pre-release documentation, specifically requiring a step-by-step tutorial of Mesos running on a single host tailored for a Developer environment. Because many developers utilize Apple hardware, a dedicated step-by-step tutorial of Mesos running on Mac OS X - Lion is also strictly required.

Furthermore, the architectural documentation needs clarification on codebase organization; specifically, the development team must reach a consensus on where the class `SharesPrinter` should reside within the source tree.

### 3.4 User characteristics

The intended users of Apache Mesos are highly technical infrastructure engineers, distributed systems researchers, and framework developers. They are typically writing code in C++, Java, or Python, which is why providing a bug-free Java Native Interface (JNI) and Python driver is so critical for the framework's adoption. They require a framework that handles complex native SDK integrations seamlessly, yet provides a stable Web UI that won't randomly crash on Ubuntu 10.04 LTS environments.

### 3.5 Programming language constraints

The primary programming language utilized for the underlying cluster manager is C++, developed originally at UC Berkeley. This requires strict adherence to memory management and careful usage of POSIX APIs.

The build tools surrounding the C++ core have specific shell constraints. The build system must eliminate the use of `pushd` and `popd` in the makefile because these commands are specific to `bash` and routinely fail when executed by standard `sh` interpreters on minimal Unix environments.

For the testing infrastructure, the C++ testing suites must be modernized. The engineering team is required to refactor `MasterTest` to use a modern test fixture pattern, standardizing the setup and teardown phases of the unit tests.

### 3.6 Process requirements

As the project matures and enters the broader open-source ecosystem, significant process requirements must be fulfilled to align with foundation standards. The project administrators must migrate users currently on the legacy Berkeley mailing lists to the official Apache mailing lists to ensure transparent communication.

Similarly, the web infrastructure must be consolidated. The team must migrate `mesosproject.org` to the Apache infrastructure, ensuring foundation-level hosting stability. During this web migration, developers must fix the broken link pointing to `<http://incubator.apache.org/mesos/>` across all official documentation.