# Apache Usergrid

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Apache Usergrid and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and database performance
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive software requirements, architectural specifications, and strategic performance targets for a highly scalable, fault-tolerant system designed to accelerate web and mobile application development. This system is engineered to provide a robust backend infrastructure, allowing developers to focus entirely on their client-side user experiences without needing to provision, manage, or scale complex server-side database clusters and API middleware.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Apache Usergrid*, and will be referred to as Usergrid in the rest of this document. It is fundamentally defined as an open-source Backend-as-a-Service (BaaS) composed of an integrated distributed NoSQL database, application layer and client tier with SDKs for developers looking to rapidly build web and/or mobile applications.  The core system has been entirely developed in the Java programming language.

The primary purpose of Apache Usergrid is to act as a foundational data and user management engine for modern applications. The mobile development community and enterprise organizations currently expend massive amounts of engineering hours rebuilding identical backend services—such as user authentication, data storage, and social graph connections—for every new application they launch. Usergrid aims to completely phase out this redundant engineering effort by providing a unified, scalable API layer backed by a massively parallel NoSQL data store.

As the project transitions into its next major lifecycle phase, the core engineering team must work out the Usergrid 2.0 Roadmap, which will dictate the architectural evolution of the platform over the coming years. This roadmap relies heavily on a massive initiative to Refactor - 2.0, reorganizing the codebase to ensure enterprise-grade stability and performance.

The high-level goals of the new framework iteration are:
a. To ensure strict compliance with foundation guidelines by importing code from the legacy github/usergrid location directly into the appropriate official repository.
b. To establish a robust integration testing environment by adding ElasticSearch and RAID capabilities directly to the PriamCluster test setup.
c. To resolve severe data presentation anomalies, specifically addressing an issue where a bad geo query incorrectly returns the entire collection of entities rather than an empty or bounded set.
d. To fortify the administrative and user management endpoints, eliminating critical application failures such as the 500 error returned by the endpoint `/management/users/{id}/confirm`.
e. To increase the stability of the client-side integrations by establishing a robust unit test framework specifically dedicated to the JavaScript SDK.
f. To prevent malicious or accidental abuse of the data layer by implementing strict system rules to limit the size of entities posted to Usergrid via the REST API.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the Backend-as-a-Service implementation:

* *ActivityStreams* – A format for syndicating social activities. Within the Usergrid system, it is a strict requirement that ActivityStreams should be indexed to allow for rapid querying and retrieval.
* *ASF* – Apache Software Foundation. The governing body for the project. The project must add license headers to all source files strictly as required by ASF policies.
* *BaaS* – Backend-as-a-Service. A cloud computing model that serves as the middleware connecting web and mobile applications to cloud services.
* *ElasticSearch* – A distributed, RESTful search and analytics engine. The system requires extensive integration testing with this technology, necessitating the setup of specific Judo Chop entry tests for UG Elastic Search, including load, search, and delete scenarios.
* *Jackson* – A popular suite of data-processing tools for Java, primarily used for JSON parsing. The system architecture requires an upgrade of all jackson dependencies to the newer `com.fasterxml.*` namespace.
* *NoSQL* – A broad class of database management systems that do not use the traditional relational database architecture.
* *SDK* – Software Development Kit. Usergrid provides client tiers with SDKs for developers looking to rapidly build applications.
* *TTL* – Time To Live. A mechanism that limits the lifespan or lifetime of data in a computer or network. The system currently experiences a bug where users are unable to set token ttl, which erroneously defaults to 604800 seconds.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the database interactions, the RESTful application layer, and the client SDK environments. Section 3 mentions other necessary considerations, including performance constraints, developer interfaces, strict process requirements, and continuous integration methodologies mandated by the Apache Software Foundation.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Java engine, the REST API, and the data indexing modules must behave during both normal operation and extreme load.

### 2.1 Apache Usergrid and its environment.

The following description outlines the intended relationship between Usergrid, the external client applications, and its surrounding compilation and execution environment:

* Mobile and web application telemetry, user data, and activity streams flow from the client SDKs to the Usergrid REST API layer.
* Developer contributions and compilation workflows flow through automated deployment systems and source control. To maintain operational continuity between legacy and modern systems, the infrastructure must maintain an automatic sync from the Github usergrid/usergrid repository directly to the Apache Git infrastructure.
* The system must be capable of being built and tested reliably on developer workstations. To support the broader development community, the build system must explicitly support Java 7 on Mac operating systems.
* The build environment relies entirely on standard Java build tools. The architecture team must overhaul all `pom.xml` files to ensure dependency trees are clean and accurate.

The main inputs to Usergrid come from application developers defining entities, relationships, and user roles via JSON payloads over HTTP. It is the job of the system's execution engine to continuously analyze and process these REST requests, validate the JSON payloads, persist the entities to the distributed NoSQL database, and deliver the correct HTTP response codes back to the client application.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the Backend-as-a-Service framework:

**Entity and Collection Management**
a. The Usergrid platform shall provide a robust and predictable entity management system. However, several critical edge cases must be resolved. Currently, providing an empty string doesn't remove an entity property, and utilizing a null value doesn't work either. The system must be updated to correctly interpret these values as property deletion commands.
b. The system must gracefully handle entity retrieval errors. A null pointer error is incorrectly returned when a non-existant property name with spaces is used in a query or retrieval request. Similarly, a null pointer response is generated when adding an entity to a collection by name. These exceptions must be caught, and proper RESTful validation error messages must be returned instead.
c. Complex character parsing within the entity engine must be stabilized. Currently, the system does not seem to be parsing '++' correctly, which corrupts data persistence and retrieval.
d. Internal asset management must respect system hierarchies. Currently, asset data does not correctly obey contextual ownership like the entity it is attached to. This poses a severe security and data integrity risk that must be remediated.

**Relational Graph and Connections**
e. The system must provide a highly scalable social graph capability. However, critical connection operations are failing. Specifically, connecting users to activities currently results in an error. This foundational social feature must be fully stabilized.
f. The system must properly enforce referential integrity during delete operations. Currently, users cannot delete an entity that has a connection to it. The framework must offer an option to cleanly delete all inbound and/or outbound connections upon an entity delete operation to prevent orphaned records.
g. The graph traversal API must return standardized HTTP responses. The `/collection/id/connected/*` paths should definitively either return an entity, an empty set, or a 404 Not Found status code, ensuring clients can programmatically handle the responses without ambiguous failures.

**Querying and Search Engine**
h. The Usergrid platform shall provide a highly expressive query language for filtering NoSQL collections. However, the query engine requires substantial optimization. Queries using the `NOT` operator are currently not efficient and cause severe database CPU spikes.
i. The query language parsing logic must be mathematically accurate. There is a documented query language issue specifically regarding numeric comparison that must be resolved to ensure filtering by greater-than or less-than operators yields accurate entity sets.
j. Advanced querying modifiers must be respected by the database adapter. Currently, applying a limit on a connection query is simply not working, resulting in unbounded payload returns that can crash client applications.
k. Geospatial querying must be optimized for speed and safety. Alongside the critical bug where bad geo queries return entire collections, the system also suffers from generally slow running and frequently timing out location queries that must be optimized at the indexing layer.

**Authentication, Authorization, and User Management**
l. The platform must provide secure and customizable identity management. The system must allow administrators to configure authentication sessions securely, fixing the bug that prevents users from setting a token TTL.
m. To support long-lived mobile sessions without forcing users to repeatedly log in, the architecture must expose a refresh token directly at the REST tier.
n. Administrative capabilities must function flawlessly across the API. Currently, a fresh Admin user token won't work on the `/management/users/me` endpoint. Furthermore, when adding an admin user, the username seems to default to the email address inappropriately, and there is a failure to recognize the 'username' property while creating an app user. These payload parsing errors must be fixed.
o. Role-Based Access Control (RBAC) must fail gracefully. If an administrator attempts to create a role without a name, the system currently throws a "funky error message" that must be replaced with a standard, descriptive validation exception.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, and developer experience requirements.

### 3.1 Reliability of the framework

Reliability of the Java core engine, the REST API, and the resulting JSON payloads has a critical priority. The system must guarantee data accuracy and operational stability, which means eliminating fatal crashes and malformed responses during data transit. A critical defect in the API serialization must be remediated immediately: the `management/token` response currently returns invalid json containing unescaped double quotes, completely breaking client-side JSON parsers.

When utilizing administrative dashboards, the system data must be accurate. Currently, the collection counters on the App endpoint are completely off, displaying entirely inaccurate aggregate totals to the developers. The internal counting mechanisms must be synchronized with the actual NoSQL data store to guarantee data consistency.

Furthermore, the system logs must be clean and actionable. The server logs are currently flooded with "No properties found for entity" warnings when simply creating an application. These false-positive warnings must be suppressed or resolved to ensure server operators can identify actual system emergencies.

### 3.2 Information volume and database performance

The system should be able to manage massive terabyte-scale datasets and millions of concurrent mobile device connections efficiently. To guarantee this level of performance at scale, the engineering team must execute rigorous load testing. The infrastructure team must setup tests to determine the precise time between load operations and search availability within the ElasticSearch cluster.

To ensure the architecture can handle high-throughput enterprise scenarios, the testing suite must perform the same load, search, and delete cycles aggressively against the system. Specifically, developers must setup the Judo Chop entry search test, the Judo Chop entry load test, and the Judo Chop entry delete test for UG Elastic Search. These tests will validate that the indexing queues do not back up under immense parallel pressure.

Furthermore, the system must improve the core query-validator modules and meticulously fix all associated test cases to guarantee that complex queries do not degrade overall database performance over time.

### 3.3 Developer interface

The community expressed repeatedly that the developer interface, SDK usability, and documentation of the system should be a major priority. The project must explicitly document semantics and provide comprehensive tutorials for deployment. Currently, basic setup is undocumented; the documentation team must add installation instructions to the official docs so that new developers can stand up a local instance of the BaaS easily.

The client-side integration experience must be frictionless across different device form factors. A critical compatibility issue must be addressed: the Usergrid Javascript SDK fails to work on the Android web browser in Android versions earlier than 4.2.2. The JavaScript SDK must be heavily polyfilled or refactored to ensure backward compatibility for legacy mobile devices.

### 3.4 User characteristics

The intended users of Apache Usergrid are highly technical mobile application developers, frontend web developers, and enterprise software architects. They are typically writing client-side code in JavaScript, Swift, or Android Java, which is why providing highly stable, bug-free SDKs that abstract away the complexity of the NoSQL database is critical for the framework's adoption. They require a framework that handles complex native database integrations seamlessly behind a friendly, highly expressive RESTful API layer.

### 3.5 Programming language constraints

The primary programming language utilized for the underlying execution engine and API layer is Java. The performance of the Java backend relies entirely on the cleanliness of its dependency tree. To ensure optimal compilation and runtime security, the framework is enforcing strict dependency management constraints.

The build tools surrounding the Java core have specific Maven constraints. The build system must be updated to add support for Maven 3.1.x and 3.2.x, ensuring compatibility with modern continuous integration environments. Furthermore, the engineering team must address deprecation warnings and thoroughly clean up declared but unused dependencies whenever executing the `mvn dependency:analyze` command.

### 3.6 Process requirements

As the project matures and transitions into the Apache Software Foundation incubator, rigorous organizational and legal process requirements must be fulfilled. The repository hygiene and legal standing of the code must be immaculate. The infrastructure team is strictly mandated to add a `NOTICES.txt` file to the root of the repository to acknowledge third-party libraries.

Furthermore, to ensure global namespace consistency with the foundation, developers must execute a massive refactoring operation to change the primary Java package namespace entirely to `org.apache.usergrid`.

Project management tools must also be properly configured. The project managers must create specific Jira components to categorize and triage incoming bug reports and feature requests effectively. Only through rigorous adherence to these ASF process guidelines can Usergrid successfully graduate to become a top-level Apache project.