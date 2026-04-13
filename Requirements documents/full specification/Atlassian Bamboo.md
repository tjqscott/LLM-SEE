# Atlassian Bamboo

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Atlassian Bamboo and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and compilation overhead
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive software requirements, architectural specifications, and strategic performance targets for a highly scalable, fault-tolerant continuous integration and continuous deployment (CI/CD) server. This system is engineered to manage automated build pipelines, abstracting the immense complexity of diverse source control managers, build tools, testing frameworks, and notification services away from fragmented command-line utilities, and presenting them as a unified, automated application backend.

### 1.1 The Project at a Glance

The software to be produced will be officially named *Atlassian Bamboo*, and will be referred to as Bamboo or "the system" in the rest of this document.

The primary purpose of Atlassian Bamboo is to act as an enterprise-grade continuous integration and continuous deployment server developed by Atlassian. The client development community and enterprise organizations currently utilize disparate tools and manual scripts for managing software build and deployment lifecycles. These legacy methods often lack coordination, reliable integration, and clear visibility. This antiquated methodology leads to massive resource underutilization, disjointed communication between development teams and operations staff, and brittle, error-prone release architectures. Bamboo aims to completely phase out this fragmented model by dynamically automating cluster resources to compile, test, and deploy code concurrently across multiple distributed build agents.

The high-level goals of the new distributed CI/CD system are:
a. To radically reduce the time and complexity it takes for developers to monitor build status by allowing the build log to be visible to anonymous users directly on the dashboard, deprecating the current standard of mandatory authenticated access for basic project visibility.
b. To increase manager and developer confidence in the repository synchronization state by undertaking a rigorous initiative to ensure complete accuracy in repository parsing; specifically, the system must ensure that CVS commit information is accurately mapped to builds, resolving instances where CVS info goes missing for some commits.
c. To increase the stability and security of the integration layer by ensuring repository credentials are secure. The system must immediately stop displaying CVS Passwords in plain text within the user interface, utilizing proper encryption or obfuscation techniques.
d. To fortify the administrative and project management endpoints against architectural changes, explicitly demanding that the system use Project IDs instead of project names in all URLs to prevent broken links when projects are renamed.
e. To ensure strict performance guarantees across the project's state by architecting the internal change detector to run asynchronously or in a dedicated queue, preventing the main application thread from locking during massive repository polling operations.
f. To provide a highly engaging and collaborative development environment by providing robust notification systems, extending beyond standard email to include the ability to configure Jabber messages for instant developer feedback upon build failures.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the continuous integration and deployment server's implementation:

* *Builder* – The mechanism executing the actual build process (e.g., Maven, Ant, Make). The architecture must natively support Bash as a default custom command builder, and ensure a version field is included within the builder configuration interfaces.
* *Continuous Integration (CI)* – The agile development practice of automating the integration of code changes from multiple contributors into a single software project multiple times a day.
* *CVS* – Concurrent Versions System. An early client-server revision control system. Bamboo requires native integration with CVS, explicitly requiring the ability to show a CVS modules drop down when selecting CVS as the source repository.
* *Fisheye* – A revision control browser and search engine developed by Atlassian. Bamboo must seamlessly integrate with it, ensuring that Fisheye change links are generated correctly without erroneously prepending the CVS status letter to the URLs.
* *Hibernate* – An object-relational mapping (ORM) framework for the Java language. The development team must prioritize the setup of Hibernate to manage the translation between Java objects and the underlying SQL database.
* *Jabber* – An extensible, open-standard instant messaging protocol (XMPP). The system must support the ability to configure Jabber messages for build notifications in the same manner that email notifications are configured.
* *Spring* – A comprehensive programming and configuration model for modern Java-based enterprise applications. The core engineering staff mandates the setup of the Spring framework to handle dependency injection and application lifecycle management.
* *Velocity* – A Java-based template engine. Bamboo uses this to generate dynamic web pages and notification emails. A condition pressed by the core staff is that the builder's Velocity context must be updated to explicitly include the `baseUrl` property, which is currently missing.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the repository adapters, the project configuration wizards, and the build queue orchestration. Section 3 mentions other necessary considerations, including performance constraints, developer interfaces, strict security requirements, and Java-centric programming methodologies mandated by Atlassian.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Java engine, the source control polling mechanisms, the build agents, and the user interface must behave during standard operation and under heavy enterprise load.

### 2.1 Atlassian Bamboo and its environment.

The following description outlines the intended relationship between Bamboo, the physical data center hardware, the source control repositories, and its surrounding network environment:

* Source code changes flow from external SCM repositories (primarily CVS and Subversion) into Bamboo's internal change detection engine.
* The change detector must run asynchronously or in a queue to prevent blocking the Java frontend; this is absolutely critical because polling large enterprise repositories will otherwise exhaust server threads and degrade UI performance.
* Build configurations are executed by distributed builder processes. These builders generate artifacts (e.g., `.jar`, `.war`, or `.zip` files) which must be retained securely on the file system. Bamboo requires that these served artifacts should respect standard MIME types when downloaded by users through the browser.
* Notification requests flow from the central execution engine to various external notification adapters. A critical configuration constraint must be remediated: the context-path is currently incorrect in notification email links, leading developers to dead web pages. Furthermore, RSS notifications are currently generating corrupted dynamic data where the feed title and author is erroneously hardcoded as 'Beetlejuice', which must be fixed to reflect actual project metadata.

The main inputs to Bamboo come from the repositories reporting code changes and the administrators defining complex build configurations. It is the job of the system's allocator to continuously analyze these inputs, generate automated trigger commands, allocate build tasks to the queue, and deliver the compiled operational directives to the designated build agents.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the continuous integration and deployment framework:

**Source Control and Repository Interaction**
a. Atlassian Bamboo shall provide mathematically accurate and highly robust repository adapter subsystems. Reliability of the repository parsing is a critical priority, necessitating an immediate resolution for the bug where CVS commit info is missing for some specific commits, breaking the traceability matrix.
b. The system must ensure that administrative configurations regarding repository viewing are strictly respected. A severe defect exists where the build setting 'ViewCVS repository module' is entirely ignored by the frontend renderer, breaking integration with external CVS viewers.
c. Complex repository workflows must be supported natively. The framework must implement advanced CVS Trigger for Branches capabilities to allow isolated feature development testing. Furthermore, the system must ensure the UI does not attempt to link 'Unknown' revision numbers to external viewers, preventing broken hyperlinks.
d. To support enterprise process requirements, the system requires extensive validation capabilities. The architecture must provide better error handling with the CVS repo, preventing the application from throwing unhandled Java exceptions when a repository is unreachable. Simultaneously, the engineering team must improve overall repository validation logic during the initial setup wizard to catch authentication errors immediately.
e. The system must be resilient against external locks. The system must gracefully resolve the critical defect where there seems to be CVS locks occurring during the Confluence project builds, which are blocking automated pipelines from proceeding.

**Project Configuration and Builder Interactivity**
f. Atlassian Bamboo shall provide highly expressive and intuitive graphical interfaces for project configuration. To facilitate non-blocking orchestration, the architecture team must allow the renaming of projects post-creation, and implement JavaScript specifically to format the project key uniformly across the application.
g. Data integrity within the build system configuration is paramount. When administrators are configuring builders, the framework must systematically make sure data is trimmed of trailing or leading whitespace, preventing hidden syntax errors in command-line arguments.
h. The project detail configuration workflow must be modernized for usability. Users want the ability to change edit project details from one massive, monolithic wizard into a series of smaller, logical forms, deprecating the disjointed user experience.
i. The system must strictly enforce configuration parameters saved by the user. A critical defect must be remediated where, on the settings page for 'Building the Project', the 'specify test directory' option isn't saved properly to the database.
j. The framework must handle trigger logic intelligently. An architectural shift is required because currently, changing a Trigger type forces a new build immediately, which wastes computing resources and should be prevented. Additionally, the architecture team must investigate an alternative to `wget` in trigger scripts to ensure cross-platform compatibility on environments without `wget` installed.

**Build Execution, Reporting, and Observation**
k. Atlassian Bamboo shall provide highly detailed distributed execution and reporting visibility. To ensure a standardized experience for open-source or public projects, the system must allow the build log to be visible to anonymous users on the dashboard without requiring an active session.
l. Database adapter stability is a critical priority during execution. A severe reliability defect regarding filesystem volume must be addressed: the system is currently creating "phantom directories" during the build execution phase, which eventually consumes all available disk inodes.
m. The queuing logic must be perfectly synchronized with the execution engine. The developers must resolve the critical regression where the Build Queue sometimes doesn't match the actual project building in the background.
n. Build observational fidelity requires an advanced logging subsystem. The core engineering team must provide a more advanced log / activity viewer within the user interface to allow developers to search through thousands of lines of compilation output effectively.
o. For local execution orchestration and testing, the system must provide the capacity to automatically generate build trigger commands that developers can copy and paste into their local terminals.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, and the complex cross-project integration methodologies mandated by Atlassian.

### 3.1 Reliability of the framework

Reliability of the Java core engine, the REST API, and the resulting notification artifacts has a critical priority. The system must guarantee operational security and data protection. A severe security defect regarding repository credentials must be remediated immediately: CVS Passwords are displayed in plain text within the configuration interface. This must be patched to obscure the passwords and encrypt them at rest.

When utilizing automated notifications, the system data must be accurate and contextually aware. A severity defect must be immediately addressed where the system is generating dynamic RSS feeds where the feed title and author is 'Beetlejuice', completely breaking the utility of RSS integrations. Furthermore, notification links must be mathematically absolute; the context-path is incorrect in notification email links, ensuring developers cannot click directly from their email to the failed build.

Project management requires flawless, non-blocking administrative workflows. Database volume must not extend initialization time for the core maintenance staff, demanding that the core staff set up standard Johnson Filter infrastructure for system-level exception management and request filtering. Furthermore, the system must be stable enough to handle massive enterprise test suites; it requires advanced reporting capabilities, explicitly demanding that the system have a list of new tests added when the number of tests in a project increase, allowing QA teams to verify test coverage.

Finally, the build engine must be robust enough to handle unexpected application states without crashing. The QA team documented an "Unusual build: Confluence stable #47" event that caused severe internal instability. The framework must be hardened to ensure unusual or excessively large build artifacts do not corrupt the server state.

### 3.2 Information volume and compilation overhead

The system should be able to manage massive terabyte-scale datasets and thousands of concurrent build artifacts efficiently. For rapid assessments of project health, the build history dashboard must be optimized for database performance, explicitly demanding that the Build history should default to the last 25 builds to prevent massive SQL queries from locking the database.

To guarantee this level of performance at scale, the user interface requires robust pagination logic. The system must provide significant capabilities to improve build number paging, ensuring that traversing hundreds of historical builds does not require loading all of them into memory simultaneously.

Visual data representations must be accurate and interpretable. Velocity charts and visualization artifacts must be mathematically precise; developers have noted that charts currently lack reference points, requiring that all generated charts should have a scale clearly marked on their axes.

### 3.3 Developer interface

The community expressed repeatedly that the developer interface, SDK usability, and documentation of the system should be a major priority. Visual interfaces must be friendly, agile, and free of clutter. The user interface must remove superfluous images & image links that distract from the core build status indicators. Furthermore, conditional rendering must be implemented accurately: the system must remove the operations column entirely if the user cannot perform any operations due to permission restrictions.

Dashboard operability requires a flawless visual environment. The development team must implement robust logic for Sorting Projects on the Dashboard so that users can prioritize failing builds. First impressions are critical for adoption; the system must implement logic to remove the link to 'log in' on the start page if you are already logged in, preventing user confusion.

Navigation must not trap the user. The UI architecture must ensure that hyperlinks are not unlinked when you are on the page they refer to, maintaining consistent menu layouts. Long strings of text must be handled gracefully by the CSS; the system currently has no wrap on the reason field, which breaks HTML table layouts.

Documentation and external linking must be accurate. A critical defect where the Help path in builder validation is hard coded with localhost:8080 must be immediately remediated so that production deployments link to the correct documentation servers. The Help icon itself is currently not working across several views and must be wired correctly. Additionally, the link to forums in the footer is wrong and must be pointed to the current Atlassian community URLs.

Finally, the system must support modern operational dashboards. Managers require the ability to externally embed full build status indicators (like badges or widgets) into external wikis or intranet portals.

### 3.4 User characteristics

The intended users of Atlassian Bamboo are highly technical software engineers, release managers, QA automation engineers, and system administrators. They are typically writing code in Java, C++, or scripting languages like Bash and Python. They rely heavily on the CI/CD server to abstract away the complexity of process management, artifact storage, and remote execution. They require an environment that feels fast and responsive, demanding that features like code compilation status and log tailing operate instantaneously without requiring manual page refreshes.

### 3.5 Programming language constraints

The primary programming language utilized for the underlying execution engine of the CI/CD server itself is Java. This mandates strict adherence to standard Java enterprise architectures.

The core engineering team requires the foundational setup of several Java-centric technologies. The system must Setup Spring to handle application wiring and dependency injection. It must Setup Hibernate to abstract the database layer and ensure cross-database compatibility (e.g., PostgreSQL, MySQL, Oracle).

Because the tooling relies heavily on templating, the socket communication and data serialization within the Velocity engine must be robust. Data serialized over this context must contain all necessary routing variables; specifically, there is no `baseUrl` in the builder's Velocity context, which must be added to allow templates to construct absolute URLs.

### 3.6 Process requirements

As an enterprise-grade tooling product, rigorous organizational testing and distribution processes must be fulfilled. The product's value proposition relies entirely on its ability to function uniformly across different operating systems and linguistic environments.

The development team must formally Setup i18n infrastructure (internationalization) to ensure that all UI strings, log messages, and notifications can be translated into multiple languages to support Atlassian's global customer base.

The QA process must heavily emphasize integration testing. The release engineering team must implement an automated matrix testing strategy that guarantees core features like SVN/CVS polling, process creation, and artifact management are verified simultaneously on Windows, macOS, and Linux prior to any public release. Furthermore, they must guarantee that URL structures remain permanent by enforcing the rule to Use project IDs instead of names in all URLs moving forward.