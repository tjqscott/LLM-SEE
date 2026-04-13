# Sonatype Nexus

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Sonatype Nexus and its environment.
* 2.2 Product functions: Repository Management and Indexing.


* 3. Other considerations.


* 3.1 Security, Proxying, and Network Reliability
* 3.2 Information Volume and Storage Optimization
* 3.3 Developer and Administrator Interfaces
* 3.4 User characteristics
* 3.5 Architectural constraints and OS Deployment
* 3.6 Process requirements and Migration Tooling



## 1. Introduction

This document delineates the comprehensive software requirements, architectural specifications, and strategic functional targets for the initial instantiation of an enterprise-grade repository manager. This system is engineered from the ground up to provide a centralized, highly secure environment for software development teams to proxy, collect, and manage their software dependencies and compiled artifacts.

### 1.1 The Project at a Glance

The software to be produced will be officially named *Sonatype Nexus*, and will be referred to as Nexus or "the system" in the rest of this document.

The primary purpose of Sonatype Nexus is to serve as a repository manager that sits between an organization's internal build infrastructure and the public internet. In modern Java development, tools like Maven download thousands of dependencies (JAR files, POMs) from remote servers. Without a centralized repository manager, builds are slow, network bandwidth is exhausted, and organizations have no control or visibility over the third-party code entering their ecosystem. Nexus aims to solve this by acting as an intelligent cache, a secure proxy, and a private hosting environment for internal corporate artifacts.

The high-level goals of this initial platform instantiation are:
a. To radically simplify developer workflows by providing native WebUI features such as Dependency copy-paste and Repository location copy-paste directly to `pom.xml` snippets.
b. To establish a robust, mathematically precise search and indexing engine that ensures version numbers are compared semantically rather than as literal strings, preventing misordered search results.
c. To provide an uncompromising, enterprise-grade proxy architecture capable of burrowing out from behind restrictive corporate firewalls (e.g., BlueCoat proxies) seamlessly.
d. To ensure flawless cross-protocol compatibility by acting as a translation layer, specifically proxying legacy Maven 1 repositories and exposing them as modern Maven 2 repositories to the internal network.
e. To deliver an intuitive administrative environment with comprehensive User management capabilities, fixing critical security flaws like ensuring the password for the HTTP proxy is properly masked with "stars" rather than displayed in plain text.
f. To facilitate frictionless onboarding for system administrators by ensuring easier installation on Linux/Unix systems, including reliable daemon wrapper scripts.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions help clarify the complex technical specifications required for the repository manager's implementation:

* *Artifact* – A file (usually a compiled JAR, WAR, or ZIP) deployed to a repository, accompanied by a POM (Project Object Model) file detailing its metadata.
* *Hosted Repository* – A repository stored locally within the Nexus server, used to deploy internal organizational artifacts.
* *Jetty* – A lightweight Java HTTP web server and Java Servlet container. Nexus will be deployed within Jetty to serve its API and WebUI.
* *POM* – Project Object Model. The XML file that contains information about the project and configuration details used by Maven to build the project.
* *Proxy Repository* – A repository in Nexus that acts as a caching layer for a remote repository (like Maven Central).
* *Snapshot* – A specific Maven versioning concept indicating a build that is currently in active development and liable to change. The system must support the automatic purging of outdated snapshot repositories to reclaim disk space.
* *Virtual Repository* – A logical grouping or translation of other repositories. The architecture requires that virtual repositories correctly return cached artifacts from their underlying source repositories.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the proxy routing, caching semantics, search indexing, and web-based artifact management. Section 3 covers critical non-functional considerations, including strict network security mandates, storage optimization, Linux/Windows daemon deployment architectures, and migration tooling.

---

## 2. Requirements description.

### 2.1 Sonatype Nexus and its environment.

The following description outlines the intended relationship between the Sonatype Nexus server, the corporate network, external public repositories, and local developer machines:

* **Internal Routing:** Developers point their local Maven `settings.xml` directly to the Nexus server. When a build requests a dependency, Nexus intercepts the request.
* **External Proxying:** If the artifact is not cached in the local `Storage directory`, the internal HTTP Proxy engine attempts to fetch it from a remote source. This requires rigorous network configuration capabilities, including binding the proxy host to a particular network device (NIC) for multi-homed servers.
* **Web Application Container:** The system operates as a Java web application. It must support flexible deployment topologies, such as being set up as a root application (`/`) within Jetty, or running under a specific context path. The architecture must guarantee that changing the Context root does not break user login functionality or RSS feeds.
* **Data Safety:** The system must interact safely with the developer's local filesystem. A critical architectural mandate is to ensure Nexus handles metadata correctly so it does not corrupt one's local repository (`~/.m2/repository`) with malformed POMs or invalid checksums.

### 2.2 Product functions: Repository Management and Indexing.

The core computational functionalities of the Nexus system are categorized as follows:

**Repository Orchestration and Proxying**

* **Repository Grouping:** Administrators must be able to group multiple repositories together under a single URL. The system must resolve the architectural defect where a newly added hosted repository cannot be grouped until the Nexus server is restarted, enabling dynamic, hot-reloading of routing rules.
* **Protocol Translation:** The proxying engine must bridge historical gaps, reliably proxying Maven 1 legacy repositories as a Maven 2 Repo, executing the necessary POM translations and directory structure mappings on the fly.
* **Third-Party Integrations:** The proxy must handle authentication challenges from external systems correctly. For example, when proxying Artifactory repositories, the system must not mistakenly cache a logon page HTML instead of the actual index when browsing group content.

**Search, Indexing, and Metadata**

* **Indexer Accuracy:** The internal Lucene-based indexing engine must be completely robust. It must resolve the critical defect where the Indexer fails to index all Artifacts, ensuring 100% discoverability. Furthermore, partial Maven archetypes must not cause problems or exceptions for index usage.
* **Search Capabilities:** The search API must correctly parse special characters, fixing the search problem when an artifact name contains a dash (`-`). To improve UX, all search results must be grouped logically, and users must have the ability to filter search results by group.
* **Remote Index Consumption:** To provide a comprehensive search of artifacts not yet downloaded, the system must support Remote Repository Access -> Download Remote Indexes, pulling down the public index catalog. When downloading these zipped indexes, the system must ensure the declared MD5 field is actually populated for integrity verification. The index updater should also intelligently use mirrors from the Maven configuration rather than constantly hitting primary public servers.
* **Contextual Search Results:** When an artifact is found, the system must ensure there are no wrong download links for snapshots in the search results. Furthermore, if an artifact exists across multiple repositories, the UI must aggregate the view gracefully, and explicitly display the source repository instead of the internal index source for the artifact being searched.

**WebUI and Developer Workflows**

* **Manual Interactions:** The WebUI must support manual Artifact upload / update workflows for proprietary libraries that are not built via CI/CD pipelines.
* **State Management:** The UI must be highly responsive to state changes. It must allow for the clearing of the artifact cache directly in the Search Results window to force a re-fetch of corrupted or stale data.
* **Settings Configuration:** Administrative toggles, such as "Allow File Browsing" and "Include In Search" within the Configuration->Repositories menu, must apply their state changes to the underlying storage router immediately.

---

## 3. Other considerations.

### 3.1 Security, Proxying, and Network Reliability

Nexus sits at the perimeter of the network, making its networking and security layers absolutely mission-critical.

* **Proxy Authentication:** The system must guarantee that the authentication of dedicated HTTP Proxy Settings for a Repository does not fail under complex NTLM or Basic Auth challenges. Furthermore, general HTTP proxy configurations must be stabilized to resolve total "HTTP Proxy not working" failure states.
* **Firewall Traversal:** Enterprise security often involves deep packet inspection or restrictive egress rules. The network adapter must implement the necessary keep-alives, chunking, and header manipulations required to burrow out from behind restrictive firewalls (like BlueCoat).
* **Input Validation & Security:** The system must defensively parse inputs. Additional URL parameters appended to requests by external load balancers or browsers should not be mandatory or cause request failures.

### 3.2 Information Volume and Storage Optimization

A repository manager will inherently consume massive amounts of disk space over time. The system must implement robust housekeeping capabilities.

* **Automated Cleanup:** To prevent the `Storage directory` from overflowing, the system must add the capability of automatic purging to snapshot repositories, wiping out non-release artifacts older than a configurable threshold.
* **Temporary File Management:** The indexing routines process massive XML and ZIP payloads. The architecture must ensure the `nexus indexer` cleans up after itself and does not leave `tmp` files behind, which leads to inode exhaustion on Linux filesystems.
* **CLI Footprint:** The distribution artifacts must be optimized. The build engineers must address the fact that the `nexus-cli` (Command Line Interface) jar is unnecessarily big, likely due to un-shaded or duplicate dependencies.

### 3.3 Developer and Administrator Interfaces

The administrative experience must be predictable, auditable, and highly legible.

* **UI Consistency:** The user interface must present correct administrative messaging. A bug must be fixed where the warning message for "Override Local Storage Location" is incorrect, which could lead administrators to accidentally overwrite critical data. Furthermore, list management must be precise; operations like "Delete selected Groups/Routes" must correctly process bulk selections, rather than removing only one item from the array.
* **Observability:** System administrators require deep visibility into the application's runtime. The architecture must allow `log4j` configuration directly via the UI, enabling admins to increase log verbosity for troubleshooting without restarting the Jetty container. To improve repository auditing, the Repositories table must add a repository policy column (Release vs. Snapshot).
* **CLI Improvements:** The Command Line Interface must be treated as a first-class citizen, ensuring that basic diagnostics, such as Version Info, are highly available in the CLI output.

### 3.4 User characteristics

The intended users of Sonatype Nexus are highly technical Build/Release Engineers, Java Developers, and Systems Administrators. They are intimately familiar with Maven POM lifecycles, transitive dependency resolution, and network routing. They require an interface that is extremely dense with data, highly responsive, and provides extensive logs. If an artifact fails to resolve, they need the UI to tell them exactly *which* proxy repository returned a 404 or a 401, rather than a generic failure.

### 3.5 Architectural constraints and OS Deployment

The primary programming language utilized for the underlying execution engine of Nexus is Java, operating within a Servlet container. This mandates strict adherence to cross-platform file pathing and memory management.

However, the deployment wrapper must integrate flawlessly with the host Operating System's init systems (Systemd, SysVinit, SMF).

* **Linux/Unix Daemonization:** The infrastructure team must resolve critical deployment blockers. The Nexus "Install as service" script does not currently work and must be refactored to support standard `/etc/init.d/` daemonization.
* **Solaris Support:** Enterprise environments heavily utilize Oracle Solaris. The standard `"nexus"` wrapper script must be patched to ensure it successfully stops Nexus on Solaris, correctly handling the OS-specific signal termination (`SIGTERM`).

### 3.6 Process requirements and Migration Tooling

As an enterprise-grade infrastructure product, rigorous organizational onboarding, documentation, and migration paths must be fulfilled. The product's adoption relies on the ease of moving off legacy tools.

* **Migration Capabilities:** The engineering team must maintain a robust Proximity Migration App to allow users of the older "Proximity" repository manager to import their data. This tool must be hardened to prevent catastrophic failures, such as crashing with a NullPointerException (NPE) during the data translation phase.
* **Documentation & Safety:** The technical writing team is strictly mandated to update documentation across the board prior to release. Furthermore, the system must defensively handle edge cases to prevent user panic, resolving UX bugs like displaying an completely empty repository list if a single repository configuration is temporarily malformed.

