# MongoDB Evergreen

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Evergreen and its environment.
* 2.2 Product functions: CI Pipelines, Patching, and Spawnhosts.


* 3. Other considerations.


* 3.1 Security, SSH Trust, and Cloud Provisioning
* 3.2 Information Volume, Logkeeper, and Core Dumps
* 3.3 Developer Interface, Dashboards, and UI/UX
* 3.4 User characteristics
* 3.5 Architectural constraints: Golang Deployment
* 3.6 Process requirements and Build State Management



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and rigorous systems-level constraints for the instantiation and ongoing development of **Evergreen** (historically referred to within MongoDB as MCI - MongoDB Continuous Integration). Engineered from the ground up, Evergreen is a distributed continuous integration system built specifically to handle the massive testing matrix required to validate the MongoDB database across dozens of operating systems, architectures, and distributed topologies.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Evergreen*, and will be referred to as Evergreen, MCI, or "the system" in the rest of this document.

The primary purpose of Evergreen is to dynamically allocate hosts to run tasks in parallel across many machines. Standard CI tools (like Jenkins or Travis CI) are fundamentally ill-equipped to handle the scale of MongoDB's testing requirements. Validating a single commit to the MongoDB core server requires compiling massive C++ binaries and running thousands of JavaScript, Python, and C++ tests against replica sets and sharded clusters. To achieve this within a reasonable feedback loop, MongoDB requires a completely bespoke, highly parallelized, elastic grid execution engine.

The high-level goals of this platform instantiation are:
a. To engineer a highly elastic cloud provisioning system that natively interacts with the AWS EC2 API, optimizing instance lifecycles by electing to stop rather than terminate idle EC2 machines to preserve AMI state and reduce boot latency.
b. To establish a flawless developer "Patch Build" workflow, allowing engineers to submit uncommitted local changes (via CLI scripts) to the distributed grid, explicitly allowing users to run arbitrary tarballs through the massive MongoDB test suite.
c. To provide an uncompromising, highly observable debugging environment for C++ segmentation faults. This requires capturing core files during test runs so engineers can debug hard crashes, supplemented by the creation of a 'symbolizer' web service to simplify examining stack traces via DWARF debug symbols.
d. To ensure strict network security and zero-trust bootstrapping for dynamic hosts. The system must completely isolate SSH credentials, ensuring that each new host spawned by MCI has a unique keyfile, and that `id_rsa` keys are never globally associated with an individual account.
e. To deliver an intuitive, visually dense administrative UI. The architecture must expose the grid, timeline, and waterfall visualizations as part of a single unified "home" view, allowing release managers to ascertain the health of the master branch instantaneously.
f. To optimize the Directed Acyclic Graph (DAG) of task execution, ensuring the system activates dependency tasks early and does not prematurely deactivate previous compile tasks if other dependent downstream tasks are scheduled.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions clarify the complex distributed systems terminology and cloud infrastructure concepts required for the CI's implementation:

* *DAG* – Directed Acyclic Graph. The mathematical model used to represent task dependencies (e.g., Task C requires Task B, which requires Task A).
* *Logkeeper* – A specialized logging server within the Evergreen ecosystem designed to handle the ingest of gigabytes of test logs from distributed agents without overwhelming the central CI database.
* *MCI* – MongoDB Continuous Integration. The legacy acronym for the Evergreen project.
* *MOTU* – Master Of The Universe. The internal codename for the central Evergreen scheduling and API server.
* *Patch Build* – A CI run initiated by an engineer using uncommitted code (a diff/patch). This allows developers to test their changes across the entire OS matrix before merging to master.
* *Spawnhost* – A dynamic EC2 instance leased temporarily to a developer for interactive debugging, provisioned with the exact OS and dependencies used in the CI environment.
* *Waterfall* – A specific UI visualization showing commits on the Y-axis and build variants (OS/Compiler combinations) on the X-axis, creating a "waterfall" of colored test results over time.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the EC2 provisioning logic, the DAG task scheduler, and the patch submission CLI. Section 3 covers critical non-functional considerations, including deep SSH trust mechanics, massive log volume management, the Golang deployment pipeline, and UI/UX optimization for data-dense dashboards.

## 2. Requirements description.

### 2.1 Evergreen and its environment.

The following description outlines the intended relationship between the central Evergreen server (MOTU), the distributed worker agents, the AWS cloud infrastructure, and the developer's local workstation:

* **The Central Server (MOTU):** A high-performance Go application containing the scheduling algorithms, the REST API, and the Web UI. It dictates the overall state of the grid and orchestrates cloud resources.
* **The Agents:** Lightweight Go binaries deployed to EC2 instances. They poll the central server for tasks, download the MongoDB source, execute the tests, and stream logs back to Logkeeper.
* **The Cloud Provider (AWS):** The system continuously monitors its queue depth and uses the EC2 API to spin up or tear down virtual machines to meet demand. The provisioning engine must be resilient; it must proactively try alternate regions on failed spawn requests if a specific AWS availability zone experiences an outage.
* **Developer Workstations:** Engineers interact with Evergreen via a CLI tool (e.g., `mci-patch`). This tool communicates securely with the MOTU server to submit diffs and request Spawnhosts.

The main inputs to Evergreen come from Git webhooks (new commits), CLI patch requests from developers, and heartbeat callbacks from provisioned EC2 hosts. It is the job of the system's execution engine to continuously analyze these inputs, resolve the DAG dependencies, dispatch tasks to appropriately tagged agents, and aggregate the resulting test telemetry into actionable data.

### 2.2 Product functions: CI Pipelines, Patching, and Spawnhosts.

The core computational functionalities of the Evergreen framework are categorized as follows:

**Task Scheduling and Dependency Management (The DAG)**
a. Evergreen shall provide an industry-leading, highly optimized task execution engine. Compiling the MongoDB C++ core takes significant time; therefore, compiled binaries must be passed downstream to integration tests. The scheduler must not deactivate a previous compile task if other dependent tasks are still scheduled, preventing redundant compilation cycles.

b. To decrease end-to-end latency, the system must activate dependency tasks early, preemptively allocating hosts for downstream tasks as soon as the prerequisite task indicates it is nearing completion.
c. Test flakiness is an inherent reality in distributed database testing (due to thread scheduling or transient network drops). The system must allow an engineer to mark a test as flaky, preventing an intermittent failure from turning the entire build waterfall red and blocking releases.

**Patch Builds and Developer Workflows**
d. The system must seamlessly accept diffs from local developer environments. The patching scripts must be mathematically robust, ensuring the `mci-patch` script is not broken by utf-8 characters in the diff set.
e. Because the MongoDB test suite requires thousands of machine-hours to run fully, the system must allow developers to limit which tasks are created when submitting a patch via the command line tool, targeting only the subset of tests relevant to their code changes. Furthermore, it must add the ability to reuse binaries in a new patch build, bypassing the compile phase entirely if the developer only modified JavaScript integration tests.
f. Once a patch is running, visibility is critical. The Patch status page should auto-refresh until complete, and the system should provide accurate visual indicators, such as ensuring the build for a patch request is turned yellow (not green) if there is still a running task. Engineers must also be allowed to explicitly indicate when a task, build, patch, or version is cancelled in its status to prevent confusion.

**Spawnhosts and Interactive Debugging**
g. When a test fails uniquely in the CI environment (but passes locally), developers require direct access to the environment. The system must provide an option to generate a Spawnhost based exactly on a failing task's environment parameters.
h. To support administrative validation of new OS images, the system must provide the ability to dry-run new build machines, verifying that dependencies (compilers, Python toolchains) are correct before inducting the AMI into the active production pool.

i. To optimize EBS storage limitations, the provisioning script must expand the root partition upon boot, removing the need for an extra block device to be mounted specifically for the massive MongoDB test data files.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including deep SSH trust mechanics, massive log volume management, the Golang deployment pipeline, and UI optimization for data-dense dashboards.

### 3.1 Security, SSH Trust, and Cloud Provisioning

Reliability of the dynamic host allocation layer has a critical security priority. Evergreen will provision hundreds of thousands of virtual machines a year; the cryptographic handshakes securing these machines must be impenetrable.

**SSH Key Lifecycle Management**
The system must establish absolute zero-trust verification for new hosts. Standard SSH clients prompt the user when connecting to a new host with an unknown RSA fingerprint. In an automated system, this prompt blocks execution. However, blindly disabling `StrictHostKeyChecking` exposes the CI to Man-In-The-Middle (MITM) attacks on the VPC.
To resolve this mathematically, the architecture dictates that Evergreen must read the host key directly from the AWS console output using the EC2 API and actively update `known_hosts` (or equivalent) on the MOTU server before attempting the first SSH connection. This ensures the system explicitly uses strict host key checking for SSH commands.

Furthermore, key sprawl must be aggressively contained. Each new host spawned by MCI should have a unique keyfile used to SSH into it, which is immediately destroyed when the host is terminated. At no point should a global `id_rsa[.pub]` key pair be associated with an individual account or shared across the grid.

**Host Callbacks**
When an agent boots, it must phone home to the MOTU server to request its payload. This callback from provisioned hosts should mathematically require a cryptographically signed secret injected via EC2 User Data, guaranteeing that rogue processes cannot spoof agent requests.

### 3.2 Information Volume, Logkeeper, and Core Dumps

The system must be engineered to manage unprecedented log datasets consisting of terabytes of stdout/stderr streams, test results, and crash dumps generated daily.

**Log Management and Optimization**
To prevent the central MongoDB backing database from being exhausted, logs must be managed efficiently. The architecture requires that logs for test failures be stored longer than we store other logs (successes), optimizing disk cost.
Network egress from the agents is costly; the system must strictly use gzip compression when serving large logs. On static or long-lived hosts, logrotation must be explicitly implemented in the MCI logging framework, or the system must routinely rotate or delete agent logs to prevent local disk exhaustion.
Furthermore, for diagnostic clarity, the architecture must add a package inventory to the system logs at the start of every task so developers know exactly which compiler and library versions were present on the host.

**C++ Core Dumps and Symbolization**
When the MongoDB `mongod` process encounters a segmentation fault, the Linux kernel generates a `core` file containing the memory state of the crash. The CI system must capture core files during test runs so engineers can debug hard crashes.
However, reading a core dump requires the exact binaries and debug symbols. The architecture team must build a dedicated 'symbolizer' web service. When a crash occurs, this service will use `gdb` and the DWARF debug symbols to translate the hexadecimal memory addresses in the stack trace into human-readable C++ filenames and line numbers, drastically simplifying the examination of stack traces for developers.

### 3.3 Developer Interface, Dashboards, and UI/UX

The community of MongoDB core engineers requires highly responsive, data-dense web interfaces to assess the health of the database branches.

**Unified Dashboards**
The user interface must be completely consolidated. The front-end engineering team must expose the grid, timeline, and waterfall views as part of a single unified "home" view. The CSS and layout must be flawless across varying resolutions; an issue must be fixed where the grid view fills with white space when the window is large, breaking the UX.

To speed up root-cause analysis, the UI must highlight a user's own commits distinctively. Furthermore, the UI must allow specific file links (e.g., core dumps or sensitive logs) to be marked as visible only to authenticated users, protecting proprietary data from unauthorized public access.

**Granular Notifications**
The system must reduce notification fatigue. Developers demand the ability to configure notifications per patch/user (e.g., Slack vs. Email), and specifically request to be notified incrementally on the completion of each patch variant (e.g., pinging as soon as Windows finishes, rather than waiting for Solaris). The `makePatchRequests.py` CLI script must also allow for user-specified notification email addresses. Crucially, for highly specific tracking, developers need the ability to subscribe directly to failures of a specific test across the entire grid.

### 3.4 User characteristics

The intended users of Evergreen are highly technical C++ database engineers, Site Reliability Engineers (SREs), and Build/Release Engineers. They are intimately familiar with Git, compiler toolchains (GCC, Clang, MSVC), and POSIX operating systems. They require an interface that is extremely dense with data, highly responsive, and provides extensive transparency. They expect to be able to add notes to task pages collaboratively during incident triage, and require the URL structure of the CI tool to be made "more sane" so they can easily share specific log lines via chat. For external tools querying the UI, the frontend must set HTTP headers for browser-side caching of static assets to ensure rapid page loads.

### 3.5 Architectural constraints: Golang Deployment

The primary programming language utilized for the underlying execution engine of the Evergreen MOTU and its agents is Go (Golang).

A critical deployment constraint must be enforced. Previously, the system was configured to execute from source. The infrastructure team must deploy built, stripped binaries of MCI processes instead of raw source `.go` files to the MOTU server. This prevents unexpected compiler variations in production, reduces startup latency, and aligns with standard immutable infrastructure deployment practices.

### 3.6 Process requirements and Build State Management

As an enterprise-grade CI product orchestrating thousands of servers, rigorous internal consistency, event tracking, and testing processes must be fulfilled.

**Data Consistency and Auditing**
The backing database (MongoDB itself) must maintain pristine state semantics. The database schema must be audited to update the string "success" to "succeeded" in the DB for absolute consistency across all collections.
The system must provide comprehensive audit trails, tracking events strictly at the version and build level, and displaying "other events" (like configuration changes or manual aborts) as lines across the commit timeline.

**Complex Repository Configurations**
MongoDB relies on multiple submodules (e.g., enterprise modules vs. open-source core). The CI system must support this explicitly. The architecture must automatically create versions in a project on update to more than one repository concurrently. Furthermore, Community build pushes should intrinsically store the corresponding enterprise build hash, allowing release managers to perfectly align the open-source and proprietary artifacts during a final release.

**Internal Testing**
Evergreen must test itself. The QA team is mandated to write comprehensive tests for the `MCI applyPatch` functionality and the `patch.go` logic, ensuring the CI never drops a developer's code. Finally, more complete unit tests for the waterfall backend must be engineered to prevent UI regression. Every action ensures that the Evergreen framework meets the strict reliability, compliance, and operational scaling requirements needed to validate the world's leading document database.