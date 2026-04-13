# Atlassian Crowd

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Atlassian Crowd and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and computational overhead
* 3.3 Developer and Administrator interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of a highly scalable, enterprise-grade Centralized Identity Management application. This system is engineered from the ground up to provide a secure, unified authentication and authorization environment, allowing enterprise organizations to manage sprawling user directories, group memberships, and application access rights from a single administrative console.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Atlassian Crowd*, and will be referred to as Crowd or "the system" in the rest of this document.

The primary purpose of Atlassian Crowd is to act as a Centralized identity management application. Currently, the enterprise software landscape is highly fragmented. IT administrators are forced to manually duplicate user accounts across disparate systems—such as bug trackers, wikis, source control repositories, and continuous integration servers. This decentralized approach creates severe security vulnerabilities, as departing employees may retain access to orphaned accounts, and password policies cannot be uniformly enforced. Atlassian Crowd aims to establish a unified security perimeter, enabling Single Sign-On (SSO) across disparate application ecosystems.

As part of the genesis of this project, Atlassian has acquired external intellectual property (formerly known as Authentisoft/IDX) to form the foundation of this tool. Consequently, a massive initial requirement of this project instantiation is to systematically change over Authentisoft/IDX text/graphics to Atlassian/Crowd branding, and update all inherited Authentisoft/IDX documentation to reflect the new Atlassian/Crowd nomenclature and standards.

The high-level goals of this new centralized identity platform are:
a. To radically simplify the user experience by providing true Single Sign-On (SSO) for domains, ensuring users only need to authenticate once to gain seamless access to all integrated web applications.
b. To act as a universal identity bridge by constructing a massive suite of connectors, including a Fisheye Connector, Jive Forums Connector, Wildfire/Openfire Connector, and a Perforce plugin.
c. To ensure a frictionless onboarding process for organizations adopting the system by engineering robust, automated data ingestion pipelines, explicitly including a JIRA user migration tool, a Confluence user migration tool, and a Jive User Migration Tool.
d. To guarantee the absolute integrity of identity data by architecting strict lifecycle management rules; specifically, the system must ensure that removing a directory aggressively removes all associated principals (groups and roles) from the database, and instantly invalidates any authorized tokens for users connected to that directory.
e. To modernize the underlying technology stack, migrating the codebase to the `com.atlassian.crowd` namespace, shifting the build system to Maven 2, and migrating source control entirely to Subversion.
f. To provide a highly extensible architecture by implementing a comprehensive Plugins System and an Event editor, allowing third-party developers to extend the identity management lifecycle natively.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the identity management platform's implementation:

* *Acegi Security* – A powerful and flexible security framework for enterprise software (later known as Spring Security). The system must provide a dedicated Acegi Connector to allow Java applications to delegate authentication to Crowd.
* *Authentisoft/IDX* – The legacy software platform that Atlassian acquired to build Crowd. All references to this legacy system must be eradicated from the source code and documentation.
* *Directory* – A repository of user and group data (e.g., LDAP, Microsoft Active Directory, or Crowd's internal database).
* *JAAS* – Java Authentication and Authorization Service. A standard Java API. Crowd must provide a JAAS Connector to allow standard Java EE application servers to authenticate against it natively.
* *OpenID* – An open standard and decentralized authentication protocol. The architecture team must explore OpenID support to allow Crowd to act as an identity provider for the broader web.
* *Principal* – A security term representing an entity that can be authenticated, which in Crowd's architecture represents users, groups, and roles.
* *Seraph* – Atlassian's open-source web authentication framework. Crowd must implement a Seraph authenticator for JIRA and Confluence to ensure native SSO capabilities within the Atlassian stack.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the directory synchronization engines, the connector architecture, and the migration pipelines. Section 3 mentions other necessary considerations, including strict security constraints, administrator interfaces, database compatibility mandates, and continuous integration methodologies required by Atlassian engineering.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Java engine, the authentication handlers, the database adapters, and the external application connectors must behave during standard operation and under heavy enterprise load.

### 2.1 Atlassian Crowd and its environment.

The following description outlines the intended relationship between Crowd, the corporate directory infrastructure (like LDAP/Active Directory), and the downstream applications relying on it for security:

* User identity data synchronizes continuously between external LDAP/Active Directory servers and Atlassian Crowd's internal database cache.
* Downstream applications (Jira, Confluence, Subversion) intercept user login attempts and forward the credentials to the Crowd server via SOAP or REST APIs for validation.
* The system must communicate flawlessly over standard web services protocols. The architecture mandates the creation of an Axis authentication handler and an XFire authentication handler to support diverse SOAP/XML client implementations.
* For domain-level security and routing, the system must ensure that DNS lookups are properly enabled for application hosts so that SSO tokens are strictly validated against the requesting server's verified IP and domain.
* The internal development environment relies on Atlassian's standard CI/CD tooling. The engineering team must get Bamboo building and running the tests for every commit to the Subversion repository to maintain absolute code quality.

The main inputs to Crowd come from applications requesting authentication tokens, administrators configuring security policies, and synchronization tasks pulling data from upstream directories. It is the job of the system's execution engine to continuously analyze these inputs, securely hash credentials, manage token lifecycles across distributed domains, and deliver strict "Allow/Deny" authorization responses in milliseconds.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the identity management framework:

**Authentication and Single Sign-On (SSO)**
a. Atlassian Crowd shall provide an unbreakable Single Sign-On environment. When a user authenticates with one connected application, they must be granted an SSO token valid for the entire domain. The system must be intelligent enough to recognize existing sessions; the architecture must fix the defect where Crowd Icon links bring up an authentication prompt when a user is already authenticated.
b. The system must support deep integration with the Atlassian product suite. The team must engineer a Confluence JIRA portlet plugin to use the Crowd security framework for authentication, allowing portlets to fetch secure data seamlessly. Furthermore, the system must provide robust performance enhancements for the legacy OSUser and Atlassian-User frameworks currently used by those applications.
c. The security engine must provide granular control. The platform requires comprehensive Security Provisioning in the Administration Console, allowing administrators to dictate exactly which applications are allowed to query which directories.

**Application Connectors and Ecosystem Integration**
d. Crowd shall not be limited to Atlassian products; it must act as a universal identity hub. The engineering team must build and maintain a massive library of connectors. This includes instant messaging and presence integrations via the Wildfire connector (also referred to as the Wildfire/Openfire Connector).
e. Collaborative and forum software must be supported, necessitating a dedicated Jive Forums Connector.
f. Source code management and developer tools must be secured. The system must natively authenticate developer actions through a Fisheye Connector and a dedicated Perforce plugin.
g. Enterprise email and communication suites must be integrated, explicitly requiring Zimbra support to ensure unified corporate communications security.

**Data Migration and Ingestion Pipelines**
h. To ensure rapid enterprise adoption, the system must provide flawless data migration utilities. Administrators cannot be expected to recreate thousands of users manually. The system must provide a dedicated JIRA user migration tool, a Confluence user migration tool, and a Jive User Migration Tool.
i. For custom legacy systems, the framework must provide a generic CSV importer.

j. Because enterprise directories contain tens of thousands of records, migrations can be time-consuming. To prevent administrators from assuming the system has frozen, the user interface must display an accurate upload progress bar when importing JIRA/Confluence users.

**Directory and Principal Lifecycle Management**
k. The system shall maintain absolute referential integrity of its security principals. A critical architectural mandate is that removing a directory must cascade correctly; the system must resolve the defect where removing a directory does not remove principals (groups and roles) from the database, which currently leaves orphaned security records.
l. Token invalidation must be absolute. The architecture must guarantee that when removing a directory, any authorized tokens for a user to that directory are immediately invalidated and no longer valid for authentication.
m. Group associations must be flawless during integrations. The system must fix the bug where adding a user through the JIVE integration API doesn't add the user to a group which is allowed to login to the application, effectively locking the migrated user out.
n. Administrative visibility must be enhanced. The interface must be updated to add the directory name when viewing a Principal (Group or Role), as administrators managing multiple directories with overlapping usernames need to know the origin of the principal. Furthermore, the system must improve searching attributes on a principal to allow for complex administrative queries.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, database compatibility requirements, and the deployment packaging necessary for an enterprise server product.

### 3.1 Reliability of the framework

Reliability of the Java application layer, the database connections, and the token generation algorithms has a critical priority. If Atlassian Crowd goes down, the entire corporate application ecosystem is locked out. The system must guarantee operational stability and security against both malicious actors and internal data corruption.

The system must be aggressively hardened against unhandled exceptions. A severe defect must be immediately addressed: when a user does not exist in Confluence and the user attempts to edit a page, a NullPointerException is thrown by the security interceptor. Crowd must return a standardized "Unauthorized" exception rather than crashing the downstream application's thread. Similarly, the system must eliminate the catastrophic bug where updating group attributes causes a crash within the Crowd backend.

General web application stability must be improved. The development team must ensure graceful error handling across the board, specifically redesigning the generic 500 page to provide administrators with actionable diagnostic logs rather than a blank error state.

### 3.2 Information volume and computational overhead

The system must be engineered to manage massive datasets consisting of millions of users, nested group structures, and instantaneous authentication requests. Because every web request in a downstream application (like loading an image in Confluence or viewing an issue in Jira) might trigger a permissions check, Crowd's database querying must be exceptionally optimized.

To support high-performance database interactions, the ORM (Object-Relational Mapping) layer must be modernized. The architecture team has noted that the `HibernateHelper` class is a little 'old school' since hibernate 3.1 came out; it is time to upgrade this to a later version to leverage modern connection pooling, caching, and lazy-loading optimizations.

Furthermore, the database adapter must support complex enterprise deployments. When using PostgreSQL, administrators require the ability to set a schema name as an attribute within the database connection configuration to conform to strict DBA (Database Administrator) multi-tenant isolation policies.

### 3.3 Developer and Administrator interface

The community of integrators and identity access management (IAM) administrators requires extensive documentation and logical, predictable interfaces.

For developers building custom connectors, the system must establish a centralized documentation repository. The infrastructure team must setup `docs.atlassian.com` for Javadoc hosting, ensuring that the Crowd API and Plugins System are fully documented and publicly accessible.

The administrative console must provide accurate licensing and metadata information. A defect must be fixed where the License Support Period is incorrect, currently showing today's date and not a year from now, which causes false license expiration warnings for enterprise clients. Furthermore, the product management team must finalize and display the official Release Date/Price information within the appropriate administrative or commercial portals.

### 3.4 User characteristics

The direct users of the Atlassian Crowd administrative console are highly technical Identity Access Management (IAM) professionals, System Administrators, and DevOps engineers. They are intimately familiar with LDAP schemas, Active Directory forests, and network security protocols. They require an interface that is extremely dense with data, highly responsive, and provides extensive audit logging.

However, the *end users* of the system (the employees logging into Jira or Confluence) should ideally never know Crowd exists. For them, Crowd must remain completely invisible, manifesting only as a seamless, instant login experience across their daily toolset.

### 3.5 Programming language constraints

The primary programming language utilized for the underlying execution engine of the Crowd server itself is Java. This mandates strict adherence to standard Java enterprise architectures, servlet containers (like Apache Tomcat), and robust security frameworks.

To modernize the application's MVC (Model-View-Controller) layer, the engineering team must upgrade to webwork 2/xwork, completely replacing legacy Authentisoft routing mechanisms with standard, secure Atlassian frameworks.

Furthermore, the deployment packaging must be meticulously curated to ensure all necessary dependencies are included. A critical packaging defect must be resolved prior to release: Spring libs are missing from the client lib folder on distribution, which breaks downstream Java applications attempting to embed the Crowd client.

### 3.6 Process requirements

As an enterprise-grade on-premises security product, rigorous organizational testing, packaging, and compliance processes must be fulfilled. The product's value proposition relies entirely on its ability to be installed cleanly across diverse operating systems.

The build and distribution pipeline must be entirely automated and modernized. The move to Maven 2 is a strict process requirement to standardize dependency management across the Atlassian stack.

The packaging of the application artifacts must follow standard conventions to prevent installation errors. The build engineers must create a sub-folder for distribution archives, so that extracting the ZIP or TAR file does not dump hundreds of files directly into the user's current directory. Specifically, the `0.3-snapshot` archive currently doesn't unpack to a sub-dir, violating standard open-source distribution expectations.

Finally, cross-platform archive extraction must be tested thoroughly. A severe unzip error on Windows environments has been identified where the archiving tool stripped the absolute path spec from `/`, causing the application directory structure to collapse upon extraction. The distribution pipeline must utilize standardized compression algorithms that respect file paths uniformly across Windows, Linux, and macOS environments. Only through rigorous adherence to these packaging and process guidelines can Atlassian Crowd be successfully deployed into highly secure enterprise networks.