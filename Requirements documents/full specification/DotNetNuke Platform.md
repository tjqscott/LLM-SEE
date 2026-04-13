# DotNetNuke Platform

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 DotNetNuke Platform and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and database performance
* 3.3 Developer and Administrator interface
* 3.4 User characteristics
* 3.5 Programming language and architectural constraints
* 3.6 Process requirements



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic performance targets for the initial instantiation of a highly scalable, enterprise-grade web content management system (WCMS) and web application framework. This system is engineered from the ground up to provide a centralized, secure, and highly extensible environment for businesses to create, deploy, and manage dynamic websites and intranets utilizing the Microsoft ecosystem.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named the *DotNetNuke Platform*, and will be referred to as DNN or "the system" in the rest of this document.

The primary purpose of the DotNetNuke Platform is to act as a premier web content management system and web application framework based strictly on the .NET Framework. In the current enterprise landscape, organizations struggle to launch and manage multiple web properties without writing custom routing, authentication, and content rendering logic from scratch for every deployment. DNN aims to establish a unified, multi-tenant digital workspace where content creation is democratized, and application delivery is standardized through a modular architecture.

The high-level goals of this new platform instantiation are:
a. To radically democratize content creation across international boundaries by implementing deep Content Localization for Taxonomy and ensuring that the framework can reliably localize module content without creating duplicate or disjointed records.
b. To provide an uncompromising, rich text authoring experience by natively integrating the TelerikEditorProvider, ensuring the `ImageEditor` operates flawlessly to empower non-technical authors.
c. To establish a highly secure, multi-tenant architecture that supports both "Host" (super-user) and "Portal" (tenant) paradigms, strictly mandating that the framework enforce a `UserQuota` on child portals to prevent resource monopolization.
d. To ensure robust aesthetic flexibility by engineering a comprehensive skinning and theming engine capable of parsing HTML5 tags as content panes, allowing front-end designers to craft modern layouts without writing backend code.
e. To deliver an unassailable installation and upgrade experience, ensuring that the installation screen never fails to load or presents a Yellow Screen of Death (YSOD), establishing trust from the very first interaction.
f. To provide granular, enterprise-grade access control by making copy permissions for page rights highly granular, allowing administrators to duplicate complex security matrices across new site hierarchies instantly.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the web application framework's implementation:

* *DarkNight* – The default, highly polished administrative and public-facing skin/theme designed for the DNN platform. The system must ensure this theme fully supports global typography, specifically handling accented characters natively.
* *Host* – The super-user or master administrator of the entire DNN installation, capable of managing multiple independent portals (websites) within a single database and codebase.
* *Object Qualifier* – A prefix applied to database tables and stored procedures to allow multiple DNN installations to share a single SQL Server database. The system must utilize a `Verify.txt` file to validate these qualifiers during deployment.
* *Partial Rendering* – An AJAX-based technique used to update only specific regions of a web page without a full postback. The architecture must ensure partial rendering functions seamlessly to provide a smooth user experience.
* *Portal* – A distinct, isolated website running within the DNN framework. The system supports a Parent/Child portal hierarchy.
* *Taxonomy* – The classification system used to categorize content. The system must ensure that the taxonomy page does not inadvertently appear twice in the navigation structure due to recursive rendering logic.
* *YSOD* – Yellow Screen of Death. The default ASP.NET error page indicating a fatal, unhandled application exception, which the DNN architecture is strictly mandated to suppress and replace with friendly error handling.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the rich text editors, the localization engines, portal management, and the skinning architecture. Section 3 mentions other necessary considerations, including strict performance constraints, administrator interfaces, data security mandates, .NET framework constraints, and deployment packaging requirements.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core C# engine, the content editors, the localization adapters, and the permission matrix must behave during standard operation and under heavy enterprise load.

### 2.1 DotNetNuke Platform and its environment.

The following description outlines the intended relationship between the DotNetNuke Platform, the end-user's web browser, the IIS web server, and the underlying SQL Server database:

* Web requests flow from the client browser into the Microsoft Internet Information Services (IIS) server, where the DNN HTTP Modules intercept the request to determine the correct target Portal and Language context.
* The system must communicate seamlessly with Microsoft SQL Server. The architecture requires that site log columns names are defined explicitly in stored procedures, ensuring that reporting tools can reliably query historical traffic and audit logs.
* To support massive enterprise rollouts with compartmentalized data, the architecture must support robust containerization. The framework must successfully generate and map containers, preventing the "Container not found" error after creating a new Parent portal.
* The internal localization engine must constantly evaluate the user's culture and language preferences. The system must implement robust extraction logic so that when an administrator extracts a language pack, it does not erroneously contain resource files of other languages.
* When content creators require rich text manipulation, the system interacts with an injected HTML Provider (like RadEditor).

The main inputs to DNN come from users typing content, navigating portals, uploading media, and configuring site permissions. It is the job of the system's execution engine to continuously analyze these inputs, manage concurrent locking, render the correct visual skin, and deliver the compiled web pages back to the requesting client efficiently.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the content management framework:

**Content Creation, Editors, and Media Management**
a. The DotNetNuke Platform shall provide an industry-leading, highly expressive rich text editor. The system must support advanced HTML components, ensuring that the RadEditor Content Filters work correctly to sanitize malicious scripts without destroying valid content structures.
b. The system must support advanced developer and technical documentation management. Within the HTML/HTMLPro Editor, the User Folder Tree must be permanently visible and fully interactive, allowing authors to navigate their digital asset libraries visually.
c. Asset management within the editor must be completely frictionless. The HTML Editor must definitively allow users to add files to new or pre-existing folders without encountering permission or routing errors. Furthermore, when editing raw markup, the HTML Source view must ensure that the vertical scroll bar is active, allowing developers to manage long documents effortlessly.

d. Content taxonomy must be user-friendly. The system must redesign the interface for categorizing content, as adding tags to Pages currently has a UX that is suboptimal; the new requirement dictates an asynchronous, type-ahead tagging interface.

**Localization and Internationalization**
e. The system shall establish a deeply integrated localization architecture. The platform must safely track translation workflows; the system must not throw an event error when querying if Content Localization (CL) is "Ready for translation?".
f. Page-level localization must be structurally sound. The architecture must prevent the anomaly where, for each language, a module "displayed on every page" is inappropriately added multiple times for a new page.
g. The onboarding experience must be globally accessible. The framework must implement complete install wizard localization, ensuring that administrators can deploy the platform in their native language from the very first execution step.

**Portal, Page, and Host Management**
h. The platform must provide robust multi-tenant lifecycle management. Administrators must have the capability to clean up infrastructure; the system must allow the Host to Manage Expired Portals effectively, archiving or destroying them as necessary.
i. Portal destruction must be an absolute and clean operation. The system must guarantee that administrators can successfully delete a Portal, wiping all associated modules, tabs, and database records without encountering foreign key constraint violations.
j. Administrative boundaries must be strictly enforced. The system should categorically not allow sub-pages to be created under the Host area by standard portal administrators, reserving the Host node exclusively for super-user global configurations.
k. Page tree management must be fluid. The architecture demands an improvement in moving pages directly from the Page settings menu, utilizing drag-and-drop or simple relational dropdowns to reparent nodes.

**Skinning, Theming, and UI Components**
l. DNN shall serve as a highly flexible aesthetic framework. The system must enforce strict skin hierarchy rules; a Splash page skin must not incorrectly override the global site skin once the user navigates past the entry point.
m. Granular design control is required. The rendering engine must ensure there is no pane level skinning failure, allowing designers to inject specific CSS classes or controls at the individual pane level, rather than just the page level.
n. Built-in skin objects must be highly configurable. The architecture must implement a Search Skin Object improvement to allow placeholder text and custom button styling, and the Text Skinobject must support changed property attributes dynamically.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, data security policies, and the .NET architectural requirements necessary for a global cloud deployment.

### 3.1 Reliability of the framework

Reliability of the ASP.NET application layer, the database connections, and the resulting HTML artifacts has a critical priority. The system must guarantee operational stability and security against malicious actors and misconfigurations.

As a web-facing application, the system will be subject to strict security protocols. The architecture must operate flawlessly in restricted environments, specifically eliminating the `EnvironmentPermission` error in hosts using modified medium trust based configurations, which is a common setup in shared hosting environments.

Authentication mechanisms must be foolproof. The system must enforce credential lifecycles accurately; the password expiry on the User Settings page must work deterministically, forcing users to reset their credentials when the policy dictates. Furthermore, the system must provide clear guidance; the Help Bubble in the Authentication System (under the Settings - Authentication Settings Tab) must appear and function correctly to guide administrators through complex Active Directory or OAuth setups.

Cross-browser compatibility is a strict mandate. The framework must ensure that Page settings are correctly displayed in Firefox, resolving previous rendering issues. The front-end output must be compliant with strict standards; the inclusion of the `autocomplete=off` attribute in `default.aspx` results in an XHTML fail, so the rendering engine must utilize compliant syntax for form security.

### 3.2 Information volume and database performance

The system must be engineered to manage massive datasets consisting of millions of user profiles, forum posts, and localized content nodes.

To support high-throughput community sites, the database adapter must be aggressively optimized. The architecture team is explicitly mandated to implement ActiveForums DB Performance Enhancements, heavily utilizing indexing and optimized stored procedures to prevent the database from locking under the load of thousands of concurrent forum users.

The core framework's instantiation logic must be mathematically highly performant. A known performance bottleneck exists in the reflection engine; developers must identify and resolve the bug in the `DotNetNuke.Framework.Reflection.CreateObject` function to ensure that dynamically loading modules does not consume excessive CPU cycles.

When presenting long-running tasks, such as site imports or upgrades, the UI must not leave the user in the dark. The system must implement an accurate asynchronous reporting mechanism so that the progress bar can show complete progress iteratively.

### 3.3 Developer and Administrator interface

The community of site administrators, module developers, and theme designers requires extensive customization capabilities and logical, predictable interfaces.

Administrative dashboards must respect access control implicitly. The system must implement robust checks so that a Dashboard page properly displays a "Visible By Administrators Only" message to unauthorized users, rather than failing to load or leaking administrative layouts. Furthermore, core administrative utilities—specifically the Portals, Users, and Event Viewer modules—must be made highly usable, leveraging modern AJAX grids for sorting and filtering.

The user profile system must be extensible. The architecture must ensure that the User Profile page is correctly registered and rendered even when using a custom template, allowing organizations to collect bespoke employee or customer data.

Finally, the UI must function under heavy optimization settings. The system must ensure that the Module action menu drop-down works flawlessly even if IIS GZip compression is enabled, requiring the JavaScript to be perfectly structured and resilient to minification and compression.

### 3.4 User characteristics

The intended users of the DotNetNuke Platform span from highly technical ASP.NET software engineers building custom modules to non-technical marketing personnel and external stakeholders managing daily content.

Because the platform will be deployed globally, its interface reliability must be flawless across devices. The system must enforce strict cross-browser CSS rules, specifically addressing CSS Issues for IE9 to ensure legacy enterprise browsers render the administrative console correctly. The framework must also prevent visual style problems in modern browsers like Firefox. Common interactive elements must be hardened; for example, the "today" button and "change the year" button must work properly on the pop-up calendar without requiring manual text entry.

### 3.5 Programming language and architectural constraints

The primary programming language utilized for the underlying execution engine of the DNN platform is C#, running on the Microsoft .NET Framework. This mandates strict adherence to standard ASP.NET enterprise architectures, WebForms/MVC paradigms, and robust relational database abstractions (ADO.NET or Entity Framework).

The deployment and packaging architecture must be meticulously configured to prevent upgrade failures. The system must gracefully handle resource files; specifically, a resource file only package (e.g., `resources-skins.zip` or `resources-modules.zip`) must not throw an error on a skin update if it is already installed, but rather perform a clean overwrite or version check.

Furthermore, the system must optimize its bandwidth footprint by ensuring that a DNN instance does not load irrelevant CSS files when a user is not logged in, keeping public-facing page weights as light as possible. When extensions are queried, the system must handle connectivity gracefully, rather than displaying an unhandled "Error: Extensions is currently unavailable" message.

### 3.6 Process requirements

As an enterprise-grade open-source product, rigorous organizational testing, packaging, and compliance processes must be fulfilled. The product's value proposition relies entirely on its ability to maintain legal compliance, accurate versioning, and transparent communication with its users.

The release engineering team must implement strict version control formatting. The build pipeline must not mistakenly leave the HTML appended with "(Alpha Version 5.6.6.1)" strings on production release binaries.

Furthermore, to ensure compliance with enterprise legal standards, the build process must systematically ensure that the copyrights on all DotNetNuke `dll` files need updating to the current release year (e.g., 2012) prior to the compilation of the final distribution archive. Every action—from the extraction of localized resource packs to the compilation of the core reflection engine—must be immutably tested, ensuring that the platform meets the strict regulatory and operational requirements of modern enterprise web development lifecycles.