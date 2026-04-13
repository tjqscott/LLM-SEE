# Atlassian Clover

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Atlassian Clover and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and compilation overhead
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive software requirements, architectural specifications, and strategic performance targets for a completely new, highly scalable Java code coverage analysis utility. This system is engineered to provide deep introspection into the testing lifecycle of Java applications, allowing software engineering teams to measure precisely which lines of source code are executed during automated test suites. By establishing this foundational framework, enterprise organizations will be able to enforce strict quality gates, reduce technical debt, and ensure that their software deployments are rigorously validated.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Atlassian Clover*, and will be referred to as Clover or "the system" in the rest of this document.

The primary purpose of Atlassian Clover is to act as an enterprise-grade Java code coverage analysis utility. As a new project instantiation, the core goal is to build a robust engine from the ground up that integrates seamlessly into modern build pipelines, integrated development environments (IDEs), and continuous integration servers. Modern Java development lacks a unified, low-overhead tool for determining test efficacy. Clover aims to fill this void by providing a highly optimized instrumentation engine that analyzes code execution at runtime without significantly degrading the performance of the underlying test suites.

The high-level goals of this new distributed system are:
a. To radically improve testing visibility by constructing a comprehensive reporting engine capable of generating new per-package coverage clouds, allowing developers to visually identify untested areas of the codebase at a glance.
b. To ensure seamless interoperability with the broader Java build ecosystem by explicitly designing native integrations, including a Maven1 Clover2 plugin, a dedicated Clover2 IDEA plugin, and a comprehensive Eclipse plugin.
c. To provide robust, mathematically precise data aggregation by engineering a backend that can accurately implement merging of per test coverage data alongside the complex implementation of merging of context registries.
d. To establish a flawless developer onboarding experience by mandating that the documentation infrastructure is hosted centrally; specifically, the team must move Clover 2 docs to Confluence to ensure collaborative authoring and maintenance.
e. To ensure absolute operational stability and prevent resource exhaustion during massive enterprise builds by guaranteeing that the system can aggressively improve memory usage during instrumentation.
f. To provide advanced historical analytics by creating a 'movers' report, which will require specialized logic for improving the handling of new classes that are added to the repository between build executions.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the code coverage server's implementation:

* *AST* – Abstract Syntax Tree. A tree representation of the abstract syntactic structure of source code. Clover will parse Java files into an AST prior to injecting coverage recording statements.
* *Bytecode Instrumentation* – The process of modifying compiled Java classes (`.class` files) to add monitoring or profiling instructions. Clover will utilize source-level and bytecode-level instrumentation to track execution.
* *CAC* – Confluence Administrator Console. The administrative interface for the documentation platform. The documentation strategy dictates that after page-ordering is implemented on CAC, the team must remove 'manual' page numbers from the documentation structure.
* *Context Registry* – An internal Clover mechanism used to filter out specific blocks of code (like logging statements or exception handling) from coverage metrics. The system requires logic to merge these registries during multi-module builds.
* *IDE* – Integrated Development Environment. Clover must operate within these environments seamlessly.
* *Maven* – A software project management and comprehension tool. Clover must integrate deeply with it, producing aggregate reports across complex, multi-module project structures.
* *NPE* – Null Pointer Exception. A common Java runtime error that the core engine must be defensively programmed against to prevent build failures.
* *Stacktrace Transformer* – A utility that will be written for Clover to translate obfuscated or instrumented stack traces back to their original, readable source code line numbers.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the instrumentation engine, the reporting mechanisms, and the data merging architecture. Section 3 mentions other necessary considerations, including strict performance constraints, developer interfaces, detailed documentation requirements, and Java-centric programming methodologies mandated by Atlassian.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Java engine, the source code parsers, the reporting adapters, and the build tool plugins must behave during standard operation and under heavy enterprise load.

### 2.1 Atlassian Clover and its environment.

The following description outlines the intended relationship between Clover, the developer's physical workstation, the build servers, and the surrounding compilation environment:

* Java source code flows from the developer's repository into the Clover instrumenter.
* During the compilation phase, Clover parses the source, injects coverage tracking counters, and outputs instrumented bytecode to be executed by the JVM.
* As the automated test suites run (via JUnit, TestNG, etc.), the injected counters record test outcomes at runtime, writing this binary coverage data to a localized database file on the disk.
* For large enterprise projects separated into multiple modules, the Clover merging engine aggregates these disparate database files into a single, unified coverage metric.
* Finally, the reporting engine reads the aggregated database and generates HTML, XML, or PDF reports for the developer interface.

The main inputs to Clover come from the source code and the configuration parameters defined in the build scripts (e.g., `pom.xml` or `build.xml`). It is the job of the system's core engine to continuously analyze these inputs, safely modify the execution paths, track thread-safe invocations, and deliver the compiled coverage directives to the reporting frontends.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the code coverage framework:

**Instrumentation Engine and Code Parsing**
a. Atlassian Clover shall provide a mathematically accurate and highly robust source code parsing subsystem. To ensure no valid Java syntax causes a compilation failure during the instrumentation phase, the engine must be rigorously tested against edge cases. Specifically, the architecture must guarantee that the instrumenter does not fail on an enum with a single semicolon in its body, a known edge case in Java 5+ parsers.
b. The system must seamlessly integrate alongside proprietary and internal codebases. To ensure zero namespace collisions during enterprise deployments, the engineering team must explicitly repackage the licensing code to avoid conflicts with internal code present in the client's environment.
c. The framework must respect complex execution contexts. The architecture team must write a robust stacktrace transformer to ensure that when an application throws an error during an instrumented test, the developer sees the correct, original line numbers rather than the modified Clover line numbers.
d. To support highly accurate reporting, the engine must natively add tracking for new coverage parameters, explicitly including `UncoveredElements` and `UncoveredBranches` within the core data model.

**Data Aggregation and Merging**
e. The new system must handle distributed and multi-module architectures flawlessly. The `CloverMergeTask` must be engineered to accurately resolve all necessary dependencies; the architecture must prevent states where the merge task can not find the `CloverDatabaseSpec`.
f. As projects scale, test suites are broken into parallel modules. The framework must implement the merging of per test coverage data securely, ensuring that thread-safe locks are utilized when combining binary coverage files. Furthermore, the system must accurately display the test results of merged databases in the final aggregate report.
g. The system must gracefully handle deprecation of legacy concepts as it establishes its new architecture. Specifically, the `testresults` element/attribute must be explicitly marked as deprecated in the new schema, guiding users toward the modern reporting structures.

**Reporting and Analytics Generation**
h. Atlassian Clover shall provide highly expressive and intuitive reporting interfaces. The core reporting task, `clover-report`, must support massive concurrency, requiring the addition of new `numThreads` and `timeout` attributes to allow administrators to tune generation performance.
i. Data representation must be advanced. The reporting engine must support the generation of new per-package coverage clouds, providing visual density maps of code coverage across the repository.
j. To maintain historical context, the system will feature a 'movers' report. This report must feature advanced heuristic logic for improving the handling of new classes introduced into the codebase, ensuring they are accurately categorized as added complexity rather than simply missing coverage.
k. The reporting engine must allow for strict filtering. The architecture must improve the default property Context filter, allowing developers to easily exclude boilerplate code (like getters, setters, and generated code) from negatively impacting their overall coverage percentage.

**IDE and Build Tool Integrations**
l. Atlassian Clover shall provide native plugins for the industry's most popular IDEs and build tools. For the Eclipse Plugin, the system must provide deep configurability, explicitly answering the architectural requirement that it can configure instrumentation output folders to something other than the main project's default classes directories, preventing output pollution.
m. For the Maven ecosystem, the system must establish a flawless Maven multi-module aggregate report engine, specifically architected to never fail to include test results from deeply nested sub-modules.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including strict performance metrics, reliability mandates, detailed documentation structures, and the complex cross-platform integration methodologies mandated by Atlassian.

### 3.1 Reliability of the framework

Reliability of the Java core engine, the instrumentation bytecode, and the resulting coverage artifacts has a critical priority. The system must guarantee operational stability and process isolation. A foundational requirement is to ensure that the system communicates cleanly with the host environment; the architecture must prevent situations where Clover dumps a lot of output to stderr instead of stdout, which would otherwise corrupt CI pipeline logs and trigger false-positive build failures.

When executing within the JVM, the system must be hardened against null references. The core logging utility must be rigorously reviewed to prevent any NPE (Null Pointer Exception) from being thrown from `Logger.getInstance()`, which would fatally crash the instrumentation phase.

Furthermore, the system must proactively assist the developer in resolving environment issues. The core runtime must detect and report classpath problems early in the build lifecycle, preventing the system from failing halfway through a multi-hour test suite due to a missing dependency.

### 3.2 Information volume and computational overhead

The system must be able to manage massive terabyte-scale codebases and millions of lines of code efficiently. Because Clover operates during the compilation and testing phases, its memory footprint must be meticulously managed.

To guarantee performance at scale, the engineering team must aggressively improve memory usage during instrumentation, ensuring that the Abstract Syntax Tree (AST) does not exhaust the JVM heap space on massive monolithic applications. Similarly, the reporting phase must be optimized; the architecture must strictly prevent any memory leak in `clover-report` when generating large XML or HTML output files.

Furthermore, the framework's configuration management must be safe for downstream consumers. The Maven integration must be architected so that builds do not fail with errors relating to JVM memory settings when entries for Clover are put in a project's parent `pom.xml` file.

### 3.3 Developer interface

The community expects the developer interface and the documentation of the system to be an absolute major priority. Because Clover is a complex enterprise tool, its documentation must be pristine, interconnected, and centrally hosted.

The documentation migration strategy dictates that the team must move Clover 2 docs to Confluence to leverage Atlassian's collaborative wiki capabilities. Once established, the documentation team must undertake a comprehensive initiative to review the Clover 2 documentation in its entirety prior to the first major release. As part of this launch readiness, the team must execute specific Clover 2 doc updates for launch, ensuring all branding and technical instructions are accurate.

The structure of the documentation must be highly organized. The team must create a comprehensive Glossary to define domain-specific terms like "Instrumentation" and "Coverage Cloud". Furthermore, specific tasks require dedicated pages: the team must add a doco page for the `<clover-format>` type (and review the Type Installation instructions simultaneously), as well as add a doco page for the `<clover-env>` task. To support new API features, the documentation must explicitly document the new test spec elements introduced in the core engine.

The onboarding experience relies heavily on tutorials. The team must critically ask "does the Tutorial need fixing?" and subsequently update the Tutorial documentation to reflect the finalized APIs. To aid local evaluation, the engineering team must create simple shell and bat scripts to run the Command Line Tools with Clover2 explicitly on the tutorial project. Additionally, they must add the Clover 1 command line tools reference to the Clover 2 docs for backward compatibility mappings.

### 3.4 User characteristics

The intended users of Atlassian Clover are highly technical Java software engineers, QA automation engineers, release managers, and system administrators. They are typically writing code in Java and managing builds via Maven or Ant. They rely heavily on the IDE to abstract away the complexity of bytecode manipulation. They require an environment that feels fast and responsive, demanding that features like coverage highlighting operate instantaneously without degrading the performance of their test suites. To support them during errors, the documentation must include a new Troubleshooting Q/A section dedicated to common integration hurdles.

### 3.5 Programming language constraints

The primary programming language utilized for the underlying execution engine of the Clover server itself is Java. This mandates strict adherence to standard Java enterprise architectures and JVM memory management practices.

The build tools surrounding the Java core have specific constraints regarding multi-module execution. The documentation team must explicitly document limitations for clover-merge specifically within Maven multi-module projects, ensuring users understand the boundaries of the architectural design.

### 3.6 Process requirements

As an enterprise-grade tooling product, rigorous organizational testing and distribution processes must be fulfilled. The product's value proposition relies entirely on its ability to be easily installed, upgraded, and referenced.

The delivery of the documentation must be multi-formatted to support offline and enterprise environments. The release team is mandated to upload the Clover 2.0 docs in PDF, XML, & HTML formats. Furthermore, intra-system navigation must be flawless: the development team must point Clover's online help directly to the live docs, and implement strict Clover docs redirection rules so that legacy bookmarks do not 404. After the Clover forums are moved to their new infrastructure, a dedicated task must update all links in the docs to prevent dead hyperlinks.

The installation and upgrade pathways must be meticulously documented. For the Maven ecosystem, the team must expand and add sub-sections to the 'Clover-for-Maven 2 User's Guide', explicitly adding an 'Installation Guide' and an 'Upgrade Guide'. Within this Installation Guide, there must be a specific mention/link to Clover-for-Maven to ensure discoverability. The core team must also re-work the Upgrade Guide collaboratively with Brendan to ensure technical accuracy.

For the Eclipse integration, process requirements dictate the creation of structured, versioned documentation. The team must create a hidden child page for the new version of the Clover-for-Eclipse User's Guide, create a hidden child page for the new version of the Clover 2.0 Upgrade Guide for Eclipse, and create a hidden child page for the new version of the Clover-for-Eclipse Installation Guide. Once the Eclipse plugin features are finalized, they must update the Eclipse Plugin installation instructions if required (pending the completion of internal ticket CEP-8).

Finally, the source code and documentation must be kept clean of draft notes prior to release. The project manager must ensure the team executes a sweep to remove comments by the end of Sept, checking with Michael first to ensure no critical architectural notes are lost. Only through rigorous adherence to these process guidelines can Atlassian Clover successfully deploy its 2.0 architecture to the global Java development community.