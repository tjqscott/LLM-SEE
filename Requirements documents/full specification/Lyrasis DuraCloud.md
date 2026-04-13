# Lyrasis DuraCloud

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Lyrasis DuraCloud and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability, Integrity, and Security
* 3.2 Information volume and Database Performance
* 3.3 Developer and Administrator interface
* 3.4 User characteristics
* 3.5 Programming language and architectural constraints
* 3.6 Process requirements



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of a highly scalable, enterprise-grade digital preservation framework. This system is engineered from the ground up to provide a centralized, secure, and highly extensible cloud-brokering environment for academic institutions, libraries, and cultural heritage organizations to preserve and compute against their digital assets seamlessly.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Lyrasis DuraCloud*, and will be referred to as DuraCloud or "the system" in the rest of this document.

The primary purpose of Lyrasis DuraCloud is to serve as a hosted service from LYRASIS that lets organizations control exactly where and how their content is preserved in the cloud. Currently, cultural heritage institutions struggle with digital preservation due to vendor lock-in, the complexity of interacting with raw cloud storage APIs (like Amazon S3 or Rackspace), and the difficulty of running necessary digital preservation microservices (like checksum validation and format conversion) at scale. DuraCloud aims to establish a unified, democratized abstraction layer. It will decouple the institution's repository from the underlying storage provider, allowing data to be seamlessly replicated, audited, and processed without downloading it back to local infrastructure.

The high-level goals of this new platform instantiation are:
a. To radically simplify multi-cloud storage management by introducing a robust `durastore` component that abstracts underlying providers, mandating the investigation of the JClouds library alongside direct EMC storage provider and Rackspace Java library integrations.
b. To establish a powerful compute layer, known as `duraservice`, which brings the processing directly to the data. This will include the provisioning of a JPEG2K Image conversion service, a Taxonfinder service, and a specialized indexing service for content search.
c. To engineer an unassailable data integrity framework, natively building a dedicated Integrity checking service that can execute on demand, relying on DuraCloud generated hashes and user-provided checksums.
d. To ensure flawless bulk data ingestion capabilities to support massive institutional onboarding. The system must natively support the New York Public Library (NYPL) in over-wire loads and verify the successful DuraCloud ingest of 10TB of Biodiversity Heritage Library (BHL) content as initial launch benchmarks.
e. To provide seamless interoperability with existing institutional repositories by engineering direct Repo-Plugins, explicitly prioritizing the Fedora/DuraCloud initial plugin and the Dspace/DuraCloud initial plugin.
f. To offer advanced, programmatic system administration and real-time monitoring via a comprehensive `duradmin` interface and a `ServicesAdmin` framework that supports the deployment of multiple instances of the same service dynamically.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the digital preservation platform's implementation:

* *AMI* – Amazon Machine Image. The virtual appliance used to create virtual machines within the Amazon Elastic Compute Cloud (EC2). DuraCloud will utilize AMIs for deployment orchestration.
* *ContentId / SpaceId* – The unique identifiers used within the DuraCloud ecosystem. A "Space" is analogous to a storage bucket or folder, and "Content" represents the digital object.
* *Duraservice* – The compute orchestration layer of the platform responsible for launching and managing microservices (like format converters and indexers) directly against the stored content.
* *Durastore* – The foundational storage abstraction layer that negotiates file streams between the user and the disparate cloud storage providers (e.g., AWS, EMC, Rackspace).
* *FUSE* – Filesystem in Userspace. A software interface for Unix-like computer operating systems that lets non-privileged users create their own file systems without editing kernel code.
* *J2K / JPEG2K* – JPEG 2000. An image compression standard and coding system favored by archives for its lossless compression capabilities.
* *Pax-logging* – An OSGi-based logging framework that allows the system to aggregate logs from various components into a unified stream.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the storage abstraction adapters, the asynchronous replication engines, and the expansive suite of compute microservices. Section 3 mentions other necessary considerations, including strict data integrity metrics, large-file performance constraints, developer interfaces, the OSGi architectural framework, and continuous integration methodologies.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Java engine, the REST API, the storage adapters, and the compute supervisors must behave during standard operation and under heavy enterprise load.

### 2.1 Lyrasis DuraCloud and its environment.

The following description outlines the intended relationship between DuraCloud, the institutional repositories, the public cloud infrastructure, and the administrative environment:

* Digital assets flow from local institutional repositories (such as Fedora Commons or DSpace) through the DuraCloud REST APIs or dedicated Repo-Plugins.
* The internal `durastore` routing engine intercepts these payloads, assesses the configured storage policies, and streams the binary data to the appropriate commercial cloud endpoint (e.g., Rackspace, EMC Atmos).
* To provide a localized, native experience for non-developer operators, the architecture demands the creation of a FUSE integration for DuraCloud, allowing users to mount their cloud Spaces directly to their local operating systems as if they were standard network drives.
* Virtual infrastructure must be heavily standardized. The system environments will be codified into AMIs. The engineering team must maintain a distinct development AMI and establish continuous integration testing strictly against the Production AMI to prevent environment configuration drift.

The main inputs to DuraCloud come from automated ingest scripts, user interface uploads, and administrative configuration updates. It is the job of the system's execution engine to continuously analyze these inputs, ensure bit-level integrity during transit, replicate data across geopolitical boundaries, and deliver the compiled storage metrics back to the requesting client seamlessly.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the digital preservation framework:

**Storage Abstraction and Content Management**
a. The DuraCloud platform shall provide a highly robust, namespace-agnostic storage engine. A critical requirement is the development of a strict ContentId / SpaceId validation library to ensure all incoming identifiers conform to URL-safe specifications.
b. The system must elegantly handle complex naming conventions inherited from legacy archives. The architecture must explicitly handle spaces and special characters in content IDs, and the parser must be hardened to ensure no errors are reported in DurAdmin when content IDs include ampersands (`&`) or double quote (`"`) characters.
c. Metadata mutability is required. Users must have the capability to execute bulk metadata and tag updates via the `StoreClient`, as well as explicitly remove metadata from an object without requiring a full re-upload of the binary payload.

**Replication and Synchronization**
d. DuraCloud shall serve as a geographic redundancy engine. The system must natively support advanced replication routines. Specifically, the framework must be able to synchronize two stores asynchronously to maintain a hot-standby disaster recovery environment.
e. The replication logic must respect the full CRUD lifecycle. The engine must actively handle replication on update/delete operations, ensuring that modifications are propagated correctly and not just appended.
f. For onboarding massive new storage environments, the system must support automated migrations, specifically executing a bulk copy from an existing store to a new/empty store without tying up the client's local bandwidth.

**Duraservice: Compute, Indexing, and Media Processing**
g. The platform must move the compute to the data. The `duraservice` module will host a suite of transformation and analysis tools. For visual archives, the system must deploy a complete JPEG2K suite, including a JPEG2K Image conversion service, a JPEG2K Image server service, and a responsive JPEG2K Image viewer service.

h. To support rapid UI rendering, a native Thumbnail generator utility must be provided to create preview images asynchronously upon ingest.
i. Domain-specific scientific tools must be supported. The framework requires the creation of a Taxonfinder service to automatically extract taxonomic names from OCR'd text documents stored in the cloud.
j. Data must be discoverable. The architecture team must engineer a highly optimized Indexing service for space/content properties/tags to support rapid search across millions of objects.
k. Service management must be highly concurrent. The `ServicesAdmin` framework must support the deployment of multiple instances of the same service to scale horizontally under heavy load, and the `ComputeManager` must be fully integrated with the `mainwebapp` for seamless monitoring.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics under massive data volume, strict reliability and cryptographic mandates, and the complex cross-platform integration methodologies required.

### 3.1 Reliability, Integrity, and Security

Reliability of the Java core engine, the REST API, and the resulting storage artifacts is the highest mandate of the system; failure to preserve data integrity negates the entire purpose of the application.

The system must guarantee cryptographic assurance. The architecture team must construct a dedicated Integrity checking service that can independently verify data at rest. This engine must be capable of checking on demand, relying primarily on DuraCloud generated hashes (MD5, SHA-256). Furthermore, to ensure data is not corrupted in transit during the initial upload, the API must allow the expected checksum value to be included when adding a content item, rejecting the payload entirely if the calculated hash does not match the provided hash.

Security boundaries must be strictly enforced. The platform must implement application security via basic authentication, ensuring that all API endpoints and UI routes are protected from unauthorized access.

System observability is critical for forensic auditing. The framework must utilize a formal Document logging framework, specifically enabling Pax-logging to standardize log outputs across all internal OSGi bundles. Finally, when errors do occur, the API must return meaningful response error codes (standardized HTTP 4xx and 5xx series with descriptive JSON payloads) rather than opaque stack traces.

### 3.2 Information volume and Database Performance

The system must be engineered to manage unprecedented datasets consisting of millions of files and petabytes of throughput. To guarantee this level of performance at scale, the engineering team must prepare the system to handle enterprise-level stress tests.

A dedicated initiative is required to create a stress testing framework specifically designed to simulate heavy institutional loads. This framework must validate that the platform remains fully responsive during a stress test of 50+ concurrent users executing massive uploads and searches.

Because storage providers like Amazon S3 have strict limits on single HTTP `PUT` requests, the `durastore` architecture must natively handle files larger than 5GB by implementing complex multipart upload protocols invisibly to the end user.

Memory management within the JVM must be mathematically rigorous. When generating manifest lists for spaces containing millions of items, the system must utilize a memory-bound Space/Content iteration technique. The iteration algorithm must employ chunking (e.g., retrieving items in pages of 1,000 using continuation tokens) to ensure the heap is not exhausted:


$$P_{total} = \lceil \frac{N_{objects}}{S_{chunk}} \rceil$$


Where $P_{total}$ is the total number of pages requested, and $S_{chunk}$ is strictly memory-bound. The architecture specifically dictates that developers properly implement `getSpaceContentsChunked()` in the EMC storage provider to comply with this mandate.

### 3.3 Developer and Administrator interface

The community of digital archivists, institutional IT staff, and repository managers requires extensive documentation and highly predictable, graphical configuration interfaces.

Administrative configurations must be dynamic. The system must support the runtime configuration of `duraservice` and `durastore` hosts, as well as the runtime configuration of DurAdmin, allowing administrators to update credentials or routing logic without restarting the Java virtual machines. Furthermore, the deployment must include a utility for `durastore` & `duraservice` initialization to bootstrap new environments seamlessly.

The Graphical User Interface (GUI) must be intuitive and comprehensive. The engineering team must ensure the `mainwebapp` UI is fully complete for the pilot, integrating the J2K viewer directly with the `duradmin` content browse interface so archivists can visually inspect high-resolution scans without downloading them.

The user management workflows must be polished. Developers are tasked to update account creation in the `mainwebapp` to streamline onboarding. The UI must proactively display service properties, so users understand the cost and status of the microservices running against their data. Finally, internal pathing must be robust; the system must initialize the `servicesadmin` `$bundle.home` variable dynamically at runtime to ensure OSGi bundles extract correctly regardless of the host OS file structure.

### 3.4 User characteristics

The intended users of Lyrasis DuraCloud are highly specialized academic librarians, digital preservationists, and IT infrastructure managers. They are intimately familiar with metadata standards (Dublin Core, PREMIS) and data sovereignty laws. They require an interface that is extremely dense with audit data, highly responsive, and provides extensive transparency. They are highly risk-averse; they do not want abstract "cloud magic," but rather explicit, mathematically verifiable proof that their digital heritage is exactly as they left it. Therefore, the visibility of checksums, transparent replication logs, and explicit error handling are paramount to user trust.

### 3.5 Programming language and architectural constraints

The primary programming language utilized for the underlying execution engine of the DuraCloud platform is Java. This mandates strict adherence to standard Java enterprise architectures, dependency injection, and OSGi bundle lifecycle management.

To maintain architectural cleanliness, the core internal communication must be standardized. The engineering team must break `RestHttpHelper` out of the `common` module to decouple REST semantics from the foundational data transfer objects.

Internal system messaging must be exhaustive. The platform must add robust messaging support for all DuraStore methods, publishing events to a message broker (like Apache ActiveMQ) whenever an object is created, updated, or deleted, allowing the `duraservice` layer to react asynchronously.

### 3.6 Process requirements

As an enterprise-grade cloud product handling sensitive cultural heritage data, rigorous organizational testing, versioning, and compliance processes must be fulfilled. The product's value proposition relies entirely on its ability to be deployed deterministically and upgraded safely.

The build pipeline must be highly organized. The build engineering team must modularize project builds using Maven, ensuring that the webapps, storage providers, and service bundles can be compiled and versioned independently. To support rapid agile iterations, the build scripts must allow for the simple updating of project version numbers across the massive multi-module POM hierarchy. Only through rigorous adherence to these process guidelines, continuous AMI testing, and strict cryptographic standards can Lyrasis DuraCloud successfully deploy its digital preservation architecture to the global cultural heritage community.