# Moodle

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Moodle and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability, Analytics, and Logging
* 3.2 Information volume and Database Architecture
* 3.3 User Interface and Experience (UI/UX)
* 3.4 User characteristics and Roles
* 3.5 Programming language and architectural constraints
* 3.6 Process requirements and Upgrades



## 1. Introduction

This document delineates the comprehensive software requirements, deep architectural specifications, and strategic functional targets for the initial instantiation of a highly scalable, open-source Learning Management System (LMS). This system is engineered from the ground up to provide educators, administrators, and learners with a single, robust, secure, and integrated system to create personalized learning environments. Built on sound pedagogical principles, the platform will facilitate online learning communities globally.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Moodle*, and will be referred to as Moodle, the LMS, or "the system" in the rest of this document.

The primary purpose of Moodle is to act as a free and open-source learning management system written in PHP and distributed under the GNU General Public License. In the current educational landscape, institutions lack a unified, cost-effective platform to host course materials, facilitate student discussions, and track academic progress. Existing proprietary solutions are rigid, expensive, and do not align with modern pedagogical theories such as social constructionism. Moodle aims to democratize online education by providing a flexible, community-driven framework.

The high-level goals of this new platform instantiation are:
a. To establish a globally accessible platform by implementing native support for languages (internationalization) from day one, allowing the interface to be localized for distinct educational regions.
b. To engineer a deeply interactive communication hub, moving beyond static file hosting to include rich, interactive modules. This includes the mandate to develop a new chat module for synchronous communication and comprehensive asynchronous forums.
c. To provide educators with unparalleled visibility into student engagement through an advanced logging system capable of producing visual graph logs of accesses.
d. To enforce modern, secure web development standards across the codebase, specifically requiring the architecture to upgrade all pages to use strict `$_GET`, `$_POST`, and `$_SESSION` variables, deprecating the reliance on insecure PHP `register_globals`.
e. To build the platform around the educator's workflow, ensuring that the system provides context-aware pedagogical tips throughout Moodle to guide teachers in constructing effective online courses.
f. To create a highly modular, extensible ecosystem where distinct learning activities—such as quizzes, polls, and assignments—can be plugged into the core engine seamlessly.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the educational platform's implementation:

* *ADOdb* – Active Data Objects Data Base. A database abstraction library for PHP. The initial architecture strictly requires an upgrade to ADOdb 2.0 to ensure the LMS can support multiple database backends (like MySQL and PostgreSQL).
* *Freetype / Freetype2* – Software font engines used to render text into bitmaps. Moodle requires the web server to support freetype and freetype2 to dynamically generate textual labels on access graphs and statistical charts.
* *LMS* – Learning Management System. A software application for the administration, documentation, tracking, reporting, and delivery of educational courses.
* *Section* – The primary structural unit of a course. The architectural nomenclature will actively clean up the use of "weeks" terminology and change it to "sections" to support courses that are topic-based rather than strictly chronological.
* *Social Constructionism* – The pedagogical philosophy underlying Moodle, positing that learning is particularly effective when constructing something for others to experience.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the course structure, the advanced forum and discussion architectures, and assignment modules. Section 3 mentions other necessary considerations, including strict database constraints, developer interfaces, UI/UX requirements, user role definitions, and the open-source continuous integration mechanisms.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core PHP engine, the database abstraction layer, the communication modules, and the student management matrices must behave during standard operation.

### 2.1 Moodle and its environment.

The following description outlines the intended relationship between Moodle, the host web server environment, the database, and the end-users:

* Moodle operates as a classic web application, designed to run on a standard LAMP stack (Linux, Apache, MySQL/PostgreSQL, PHP).
* The application interfaces with the database entirely through the ADOdb 2.0 abstraction layer, preventing vendor lock-in and allowing institutions to utilize their existing database infrastructure.
* The system must communicate flawlessly with external mail servers to facilitate notifications. The environment must be highly configurable, allowing administrators to allow PHP mail as well as external SMTP mail routing.
* Content creation flows from the educator's web browser into the PHP application layer. To facilitate this without requiring educators to write HTML, the system must add a full editor for text-entry forms (postings, course descriptions, etc.).

The main inputs to Moodle come from teachers defining course structures, students submitting assignments, and users engaging in forum discussions. It is the job of the system's execution engine to securely process these inputs, manage course enrollments, calculate grades, and deliver structured, styled HTML pages back to the user.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the educational framework:

**Course Structure and Content Delivery**
a. The Moodle platform shall provide a highly flexible course layout engine. To support diverse teaching styles, the system will group content into modules. The UI must provide clear navigation between modules (via a popup menu or breadcrumb trail) to ensure students do not get lost.

b. Instructors must have granular control over course pacing. The architecture must add switches to allow teachers to show one week (or section) at a time, preventing students from feeling overwhelmed by the entire syllabus at once.
c. Page formatting must be pristine from the root level down. The system must ensure the strict formatting of the site home page, acting as an inviting portal for the institution. Furthermore, editing capabilities must be frictionless; the UI will add an editing switch to all relevant pages (specifically in the top-right corner) so authenticated teachers can toggle between "view" and "edit" modes instantly.

**Forums, Discussions, and Asynchronous Communication**
d. Moodle shall establish a deeply integrated, hierarchical communication architecture. A critical distinction must be made in the data model: the system must formally split out "forums" (the container) from "discussions" (the individual threads). The UX team must ensure the interface clarifies the difference between a discussion and a forum, as overlapping terminology is confusing to users.

e. Forum engagement must be highly trackable. The system must provide a specific report for the analysis of discussions to help teachers grade participation. Furthermore, the system must add the capability to search all discussions across the platform globally.
f. Post management must mimic modern bulletin boards. The system must implement user forums for general socialization. Within any discussion, the system must allow one attachment per discussion post to facilitate document sharing.
g. Data integrity within the forums is paramount. When a user updates a discussion topic post, the system must automatically update the discussion name in the database. To ensure a fluid UX, after adding a reply to a discussion, the routing engine must return the user to their post in context, rather than dumping them at the top of the page.
h. Teachers require ultimate authority over communication channels. The permissions matrix must allow a teacher to delete any posting within their course. Furthermore, teachers must be able to see a list of subscribers to each forum, and possess an administrative button to force-subscribe everyone to a forum for critical announcements.

**Assignments, Assessments, and Modules**
i. The platform must provide robust tools for evaluating student performance. The system requires a dedicated module to submit assignments digitally, replacing physical drop-boxes.
j. Feedback loops must be tight. The assignment summary page must include teacher remarks directly alongside the grade, ensuring students understand their evaluations.
k. For rapid, informal feedback, the system will include a Choice (poll) module. The database schema for this module must be expanded to support at least 6 choices, providing enough variability for standard classroom polls.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including telemetry, data visualization, strict administrative interfaces, user role boundaries, and the open-source upgrade methodologies required for the project's success.

### 3.1 Reliability, Analytics, and Logging

Reliability of the PHP application layer, the database connections, and the resulting user telemetry has a critical priority. Educational institutions require legally sound records of student attendance and activity.

The logging system must be meticulously designed. The engineering team is tasked to heavily improve the logging system to capture every read and write action performed by any user. To make this data actionable, the platform must utilize the Freetype libraries to dynamically graph logs of accesses, providing teachers with visual histograms of student engagement.

Administrative oversight relies on these logs. The architecture must improve logs so that a site administrator can see all courses from a single unified report. To ensure these reports are usable, the UI must add sorting (asc and desc) capabilities on the full report tables. Additionally, to foster a sense of community, the system will add activity and log links directly to public user profile pages.

### 3.2 Information volume and Database Architecture

The system must be engineered to manage datasets spanning thousands of users, tens of thousands of forum posts, and continuous access logs. The reliance on ADOdb 2.0 ensures that SQL queries are optimized for the specific dialect of the underlying database (e.g., handling pagination and date formatting correctly across MySQL and Postgres).

Email notifications will generate significant outbound volume. The notification engine must execute `email.php` securely and efficiently, ensuring it utilizes the new, optimized email system. To accommodate user preferences, the engine must add support for HTML mail (making it user-selectable so users on low-bandwidth connections can opt for plaintext). For critical onboarding, the system will automatically send a welcome email when a user enters a course for the very first time.

### 3.3 User Interface and Experience (UI/UX)

The community of educators and students requires intuitive, accessible, and highly responsive interfaces. The design system must be cohesive. A major architectural task is to revamp styles throughout the system, moving away from hardcoded HTML attributes toward centralized Cascading Style Sheets (CSS).

Cross-browser compatibility is a strict mandate in the diverse educational sector. The frontend engineering team must ensure the CSS is robust, specifically addressing issues where styles look odd on Internet Explorer, which is heavily utilized in public school computer labs.

### 3.4 User characteristics and Roles

The intended users of Moodle span from highly technical site administrators to teachers, and down to students of varying technical literacy. The permissions matrix must strictly separate these personas.

**User Profiles & Identity**
The system must maintain rich user profiles. The database must be updated to add missing user profile options, and the UI must provide a persistent reminder to fill in the profile page if a user has left mandatory fields blank. Global coordination requires temporal awareness; the system must add timezone configurations to user preferences so assignment deadlines display correctly for international students.

**Role Definitions**
The system must formalize the guest student system, allowing anonymous or read-only access to specific public courses without requiring full matriculation.
For educators, the platform must respect academic hierarchies by supporting Teacher titles and ordering within the course display.
To facilitate collaborative learning, the architecture mandates the implementation of groups for students, and the subsequent use of these group structures in all activities (so a forum can be restricted to just "Group A").
Finally, for troubleshooting, the administrative role must possess a highly secure `loginas` capability, allowing the admin user to impersonate any student or teacher to diagnose permission errors.

### 3.5 Programming language and architectural constraints

The primary programming language utilized for the underlying execution engine of the Moodle platform is PHP. This mandates strict adherence to web security standards.

As noted in section 1.1, the most critical architectural constraint for the v1.0 milestone is the deprecation of legacy PHP variable handling. The engineering team must painstakingly upgrade all pages to use `$_GET`, `$_POST`, and `$_SESSION` variables exclusively. This prevents variable injection attacks and ensures compatibility with modern PHP configurations where `register_globals` is disabled by default.

### 3.6 Process requirements and Upgrades

As an enterprise-grade open-source product distributed under the GPL, rigorous organizational versioning, distribution, and community management processes must be fulfilled. The product's value proposition relies entirely on its ability to be safely upgraded by disparate IT departments worldwide.

The upgrade methodology must be automated. The architecture must provide robust XML-based or SQL-based migration scripts to fix up Moodle main upgrades from version to version. Furthermore, because the system is modular, it must include an internal API to handle module self-upgrades independently of the core framework.

Community contribution is the lifeblood of the project. The infrastructure team must create `cvs.moodle.com` for the public web display of the source code repository. To track ongoing development, the project relies on a dedicated Bug Tracker, which must be maintained diligently (and patched when it experiences a bug during the posting of comments). Finally, to acknowledge the open-source community, the platform's administrative interface will feature a dedicated contributions page, which must be kept formatted and up to date. Every action must ensure that Moodle meets the strict pedagogical, regulatory, and operational requirements necessary to become the world's leading open-source learning management system.