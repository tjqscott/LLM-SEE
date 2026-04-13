# Atlassian Software Server

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Atlassian Jira Software Server and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and computational overhead
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive software requirements, architectural specifications, and strategic functional targets for a proprietary, server-based issue tracking and agile project management product. The system is engineered to provide a centralized environment for bug tracking and agile methodologies, abstracting complex workflows, reporting structures, and board management away from fragmented utilities, and presenting them as a unified application backend.

### 1.1 The Project at a Glance

The software to be produced will be officially named *Atlassian Jira Software Server*, and will be referred to as Jira or "the system" in the rest of this document.

The primary purpose of Atlassian Jira Software Server is to act as a proprietary issue tracking product developed by Atlassian that allows bug tracking and agile project management. The client development community and enterprise organizations currently utilize disparate tools for bug tracking that often fail to incorporate agile practices smoothly into their workflows. This antiquated methodology leads to massive project management underutilization, disjointed visibility between development teams and management, and brittle operational architectures. Jira aims to phase out this fragmented model by dynamically shared issue tracking resources among various distributed computing frameworks and methodologies.

The high-level goals of the new distributed systems are:
a. To radically reduce the time and complexity it takes for developers to maintain and update the status of agile tasks by introducing the ability to go directly to the issue edition screen from the agile card, deprecating the current standard of multi-click navigation.
b. To increase manager and developer confidence and visibility in the product state by introducing the capability to see the Description of the Issue behind the card via a "Zoom In" large card view, which currently requires navigating away from the planning or task boards.
c. To reduce the repetitive and error-prone boilerplate code required to generate new requests by allowing managers to create new Issues on a card-like view, simplifying the initial data capture phase.
d. To fortify the administrative and project management endpoints, eliminating critical application failures, specifically addressing an issue where the Chart board breaks when using context options such as Filtering or the "Assign to me" checkbox.
e. To ensure strict consistency guarantees across the project's state by ensuring the system can detect inconsistencies for orphan issues in the case of parent-child versions, protecting the integrity of the release roadmap.
f. To provide a highly engaging and cloud-connected onboarding experience by providing a new suite of permanent context tools, ensuring that users have the possibility to highlight the cards based on specific criteria for rapid assessment.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the issue tracking and agile management kernel's implementation:

* *Anonymous User* – A user navigating the system without active authentication. The system must ensure that the menu bar links are fixed for these users to prevent dead-end navigation.
* *Burndown Chart* – A dynamic graphical representation of work left to do versus time. The system must support the ability to configure these charts using multiple statistics, though a critical failure where some change logs are counted twice must be immediately remediated.
* *Closed Issue* – An issue status indicating that a task is complete. To protect the integrity of historical data, these issues should not be editable; therefore, when moving a parent task, the updating box must not include or allow editing of closed subtasks.
* *GreenHopper* – The proprietary agile project management plugin (later known as Jira Software) being specified and integrated deeply into the Jira core in this document.
* *Mandatory Fields* – Fields that must be populated before a specific action can be completed. The framework must support adding a screen in a transition specifically to support and enforce these fields during the agile workflow.
* *Permlink* – Permanent link. An immutable URL pointing to a specific resource within the application, which the system must support creating to improve collaborative visibility.
* *Subtask* – A child element of a parent issue used to break down work. The architecture team must ensure that time tracking effectively integrates these, explicitly demanding that the system supports aggregate time tracking for parent and subtasks within the current release cycle.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the agile card interfaces, the mathematical chart logic, and the board environment constraints. Section 3 mentions other necessary considerations, including performance constraints, developer interfaces, strict process requirements, and cross-project integration methodologies.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Java engine, the REST API, the agile card interfaces, and the database adapters must behave during operation.

### 2.1 Atlassian Jira Software Server and its environment.

The following description outlines the intended relationship between Jira, the local developer's operating system environment, and the surrounding network environment:

* Workload execution requests flow from user-defined frontends, text editors, or CLI tools to the local web server layer.
* During the integration phase, processed scripts and styles are scanned by the system and appended to the final CSS and script source files.
* Data visualization artifacts flow from the backend calculation engine to the front-end chart components. A severe browser-specific defect must be remediated: memory is currently leaking specifically in Internet Explorer 7 (IE7) during these operations, which must be immediately fixed to prevent application failures on supported browsers.
* The GreenHopper plugin architecture acts as an extensible wrapper around the core Jira application. To ensure a standardized experience, GreenHopper should show the same links in the main menu bar as when browsing any other page within the Jira core application, deprecating disjointed navigation.
* As a specialized enterprise integration, the framework must introduce robust support for other Atlassian products, specifically requiring the implementation of a static portlet for Confluence.

The main inputs to Jira come from the users defining issues, estimates, and roadmap versions. It is the job of the system's execution engine to continuously analyze and process these offer, generate standard chart visualization messages based on them, and deliver the compiledoperational directives to the distributed nodes.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the agile management and bug tracking framework:

**Agile Card and Board Interactivity**
a. Atlassian Jira Software Server shall provide a highly responsive, non-blocking agile board interface. To facilitate rapid updates, the architecture team must implement the capability to dynamically update issues from the agile cards, ensuring that developers are not forced through complex multi-click navigation.
b. The agile cards must be mathematically precise visual metaphors. A structural defect must be remediated: the card height needs a rigorous fix specifically when adding a comment to ensure layout integrity.
c. The cards must act as the primary interface for relational management. Users want to be able to change the component of an issue directly from the card within the VersionBoard. Furthermore, the system must allow a user to change the version of their issue directly from the card within the ComponentBoard environment.
d. To support the broader development community, the agile card interface requires an expansive set of corner fields. The team must update the cards to support multiple corner fields, rather than the current fixed limitations of only 2 or 3 fields, ensuring organizations can display necessary metadata at-a-glance.

**Chart Generation and Time Tracking Mathematical Logic**
e. Atlassian Jira Software Server shall provide mathematically accurate visualization reporting subsystems. Reliability of the charts has a critical priority, necessitating an immediate resolution for the bug where charts count some change logs twice, causing the burndown chart to "burn too many hours" and provide entirely inaccurate velocity data.
f. Chart integration must be flawless during administrative events. Previously, an exception was thrown while trying to display a chart immediately after a JIRA upgrade; this upgrade-path stability must be hardened. Furthermore, the Chart Board currently breaks completely if we click on "Assign to me" or on the "Filter" checkbox, which must be remediated.
g. The system must precisely manage time tracking across the hierarchy. To support detailed estimation logic, the core engine must support aggregate Parent and Subtasks timetracking, allowing managers to see accurate totals.
h. The Burndown Chart calculation engine must be perfectly synchronized with external dependencies. Critical defects are currently documented: Editing worklogs is bringing incorrect results in the Charts. Worklogs on the release date are not computed in the burndown chart at all. Finally, if logging work on an Issue that wasn't originally estimated and estimating it at the same time, the chart board won't reflect the reestimation; these gaps in logic must be closed.
i. The framework must implement a dedicated velocity tracking capability to allow teams to programmatically assess historical throughput.

**Roadmap and Workflow Orchestration**
j. Atlassian Jira Software Server shall provide extensive, non-blocking roadmap management interfaces. Users must have the capability to edit the Version release date within the Planning Board directly, rather than being forced back into administrative contexts.
k. For flexible project management, the system must establish the possibility to override the working days in a sprint, allowing for non-standard organizational schedules. Furthermore, the system must allow managers to set a dynamic capacity for their Versions based on a chosen statistic.
l. To support enterprise process requirements, the system must allow project leads and components to be edited within the planning environment directly.
m. Workflow enforcement must be airtight. The framework must not only support workflow screens in the Task board transitions but also mandate a specific screen to support Mandatory fields during transitions to protect data integrity.

**Querying, Filtering, and Dashboard Interoperability**
n. The Jira platform shall provide a highly expressive query language for filtering collections. However, the query engine requires substantial optimization. Users require robust filtering capabilities, explicitly requiring that a manager or developer can filter issues based on component criteria seamlessly within the GreenHopper view.
o. Advanced querying modifiers must be respected. The Component board select list is currently broken, presenting Versions inappropriately instead of the components; this query selection error must be fixed. Furthermore, attempt to remove filters from the chart board currently generates a definitive HTTP 404 error, which must be remediated.
p. Dashboard interoperability is paramount for modern operations. The framework must implement burndown chart portlets to create a multi-project dashboard, ensuring managers can aggregate visibility across their entire release organization.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, and the complex cross-project integration methodologies mandated by Atlassian.

### 3.1 Reliability of the framework

Reliability of the Java core engine, the REST API, and the resulting chart visualization artifacts has a critical priority. The system must guarantee mathematical accuracy and operational stability, which means eliminating fatal crashes and duplicate change logs during data transit. A critical defect in the API serialization must be remediated immediately: the system currently throws an exception while trying to flush user properties inappropriately.

When utilizing administrative dashboards, the system data must be accurate. A severity defect in the browser rendering must be immediately addressed: memory is leaking specifically in IE7, requiring that the architecture team investigates and patches these leaks immediately to prevent browser-level failures. Furthermore, when attempting to remove filters from the chart board, the system currently yields a generic HTTP 404 error that must be replaced with a standard, descriptive validation exception.

Project management requires flawless visual artifacts. The engineering staff did not express an opinion on visual branding choices, provided that the system can fix the critical defect where the logo doesn't load properly within the user interface. Furthermore, the application requires comprehensive browser parity; specifically, the menubar is broken with Firefox and must be entirely reconstructed to ensure stability across platforms.

### 3.2 Information volume and database performance

The system should be able to manage massive terabyte-scale datasets and thousands of concurrent browser connections efficiently. To guarantee this level of performance at scale, the internal counting mechanisms must be synchronized with the actual NoSQL data store to guarantee data consistency.

As projects grow to encompass hundreds of files and thousands of active requests, visual performance becomes critical. When editing worklogs, the system must meticulously calculate the impacts to Charts, eliminating the current regression where duplicate change logs corrupt velocity statistics. Furthermore, the system logs must be clean and actionable; any exception thrown while displaying a chart must be caught and remediated to ensure server operators can identify actual system emergencies.

To support the massive volume of data associated with enterprise roadmaps, the framework requires a sophisticated strategy for data volume. To assist developers in rapid prioritization, the system must allow a manager or developper to see the Description of the Issue behind the agile card (e.g., via a Zoom In or large card metaphor) without requiring a full page reload or full navigation.

### 3.3 Developer interface

The community expressed repeatedly that the developer interface, SDK usability, and documentation of the system should be a major priority. The project must explicitly document semantics and provide comprehensive tutorials. Users explicitly require enhanced navigability from JIRA from the main navigator and from the roadmap interfaces seamlessly.

The user integration experience must be frictionless. For rapid reporting, the platform requires an advanced set of collaborative visibility capabilities, explicitly demanding that a GH user can print the task board and the chart board. Furthermore, the framework must provide a robust set of permlinks, ensure specialized multi-lingual special characters are rendered properly on all visual labels, and allow for standard configuration pages and print-ready formats.

### 3.4 User characteristics

The intended users of Atlassian Jira Software Server are highly technical software engineers, data scientists, and machine learning infrastructure engineers. They are typically transitions into mobile development, enterprise software architects, and independent software vendors (ISVs). They require a framework that handles complex native database integrations (like CUDA and cuDNN) seamlessly behind a friendly, highly expressive RESTful API layer. They require an environment that is optimized for speed and safety, ensuring complex data visualization artifacts are highly expressive and mathematically accurate, providing the flexibility to configure fields shown on the summary view of cards.

### 3.5 Programming language constraints

The primary programming languages utilized for the underlying execution engine of Jira Software Server are proprietary Java and JavaScript. As a proprietary product, the core staff maintains control over all underlying grammar and implementation choices. The target Java version must be updated, implicitly requiring support for the underlying JIRA 3.11 features for aggregate Parent and Subtasks time tracking.

### 3.6 Process requirements

As the project matures and maintains its status as an enterprise product, rigorous process requirements must be fulfilled. The product's value proposition relies entirely on its ability to function uniformly across different operating systems. The core maintainers shall manage repository hygiene and legal standing, as conditions pushed by the core engineering staff did not express an opinion on visual branding choices, provided that the select components in the component board are fixed immediately. Project managers must manage proper triage, explicitly demanding that the project managers must merge the GreenHopper JIRA Project with the GreenHopper Support Project to ensure standardized bug reporting. Finally, educational resources must be front-and-center, requiring the team to provide comprehensive steps for distributed training and documentation.
