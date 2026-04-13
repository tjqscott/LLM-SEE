# Aptana Studio

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Aptana Studio and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and computational overhead
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive software requirements, architectural specifications, and strategic performance targets for a highly integrated development environment (IDE). This system is engineered to provide a robust, cross-platform workspace that empowers developers to rapidly author, debug, format, and execute advanced web applications and Python-driven backend scripts without relying on fragmented command-line utilities.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Aptana Studio*, and will be referred to as the Studio or Aptana in the rest of this document.

The primary purpose of Aptana Studio is to act as an open-source integrated development environment (IDE) explicitly designed for building advanced web applications. While the broader objective encompasses comprehensive web development, the initial architectural phases are heavily concentrated on providing robust support for dynamic scripting languages, specifically Python, integrated directly into the Eclipse Rich Client Platform.  The client development community currently utilizes basic text editors that lack deep syntactic introspection, leading to frequent runtime errors and poor developer productivity. Aptana Studio aims to completely phase out these rudimentary tools by providing a rich, natively integrated developer experience with deep code intelligence and an interactive debugging suite.

The high-level goals of the new IDE are:
a. To radically improve code authoring and readability by completely overhauling the editor's text manipulation engine, ensuring that indentation formatting—such as spaces-for-tabs on multi-line indents—behaves predictably across all operating systems.
b. To streamline project navigation and workspace management by introducing dynamic resource filtering, such as the ability to utilize a filter in navigation specifically for removing compiled `*.pyc` files from the developer's visual workspace.
c. To provide robust, real-time debugging capabilities that allow developers to step through complex execution flows, requiring the implementation of advanced features like "break for exception" and reliable breakpoint initialization.
d. To create a highly engaging, intuitive user interface that leverages native IDE paradigms, including the ability to double-click to select a valid Python identifier and utilize Control-Click on a function for instant hyperlinking to its definition.
e. To ensure absolute operational stability of the underlying platform by addressing critical catastrophic failures, such as resolving the fatal defect where Eclipse completely closes on save.
f. To distribute the application reliably across all major developer workstations, necessitating rigorous cross-platform compatibility testing for the code completion engine on Linux, Mac OS X, and Windows XP environments.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the Integrated Development Environment's implementation:

* *AST* – Abstract Syntax Tree. A tree representation of the abstract syntactic structure of source code. The Studio relies on parsing source code into an AST to populate the Outline view with class attributes and fields.
* *Code Completion* – An intelligent predictive typing feature (often referred to as Content Assist) that suggests variable names, methods, and keywords as the developer types. Aptana utilizes a background socket mechanism to process these completion requests.
* *Code Folding* – A feature of the graphical text editor that allows users to selectively hide and display sections of a currently-edited file as a part of routine editing operations.
* *Eclipse RCP* – Eclipse Rich Client Platform. The underlying Java-based framework upon which Aptana Studio is built, providing the plugin architecture, window management, and core editor capabilities.
* *Socket* – An endpoint of a two-way communication link between two programs running on the network. The Studio uses a Code Completion socket to communicate between the Java Eclipse frontend and the Python backend parser.
* *Syntax Highlighting* – A feature of text editors that displays text, especially source code, in different colors and fonts according to the category of terms. The framework requires bold and new categories of syntax highlighting to distinguish complex language constructs.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the intelligent code editor, the code completion engine, and the complex remote debugging mechanisms. Section 3 mentions other necessary considerations, including strict platform compatibility, process lifecycle management, Java packaging constraints, and reliability mandates.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core IDE process, the code parsers, the inter-process communication sockets, and the debugging pipelines must behave during operation.

### 2.1 Aptana Studio and its environment.

The following description outlines the intended relationship between Aptana Studio, the local developer's operating system environment, and the underlying language runtimes:

* Aptana Studio launches as a heavy graphical desktop application on Windows, macOS, or Linux workstations, operating as a sophisticated suite of plugins operating within the Eclipse 3.0 ecosystem.
* As the developer types, integrated parsers within the Studio monitor the local file system and text buffers, instantly analyzing scripts to provide real-time syntax highlighting, brace matching, and Code Completion suggestions.
* The Studio interacts securely with the underlying operating system to spawn external execution processes. When a developer triggers a debug session, the IDE orchestrates the creation of a Python process and attaches an interactive debugger to it via local network sockets.
* The IDE provides comprehensive update mechanisms to ensure the developer is always utilizing the latest tooling, communicating with an external Discovery site to pull new plugin versions.

The main inputs to Aptana Studio come from developer keystrokes, configuration selections, and file system interactions. It is the job of the IDE's core dispatcher to continuously analyze and process these inputs, format the text accurately, manage project manifests, and orchestrate the complex underlying execution engines without blocking the graphical user interface.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the IDE framework:

**Intelligent Text Editing and Formatting**
a. Aptana Studio shall provide an industry-leading text formatting engine that strictly adheres to dynamic language indentation rules. The system must ensure that autoindent works reliably after a comment line, preventing developers from manually realigning their logic blocks.
b. The handling of whitespace must be mathematically precise. The editor must strictly enforce spaces-for-tabs rules, specifically ensuring this functionality is not broken on multi-line indents. Furthermore, tabs inserted within a line must be accurately replaced with spaces based on the user's defined tab-width preferences.
c. The text manipulation engine must be safe. A critical destructive bug must be remediated where the editor deletes a line completely when the user presses `SHIFT + SPACE`. Similarly, the system must ensure that triggering an uncomment action does not accidentally remove lines of code.
d. Visual text assistance must be comprehensive. The editor must highlight the matching brace when the cursor is positioned near a parenthesis or bracket, aiding in the comprehension of deeply nested logic. The system must also support robust code folding, ensuring there is no error in the code folding calculations that would cause the editor to hide the wrong sections of text.

**Code Intelligence and Navigation**
e. The Studio must provide deep code introspection. The Outline view must accurately parse the source file and show class attributes and fields, allowing developers to visually map the structure of object-oriented code.
f. The code completion engine must be universally functional. The system relies on a background socket to process completion logic; the engineering team must resolve the architectural defect where the Code Completion socket won't open, completely breaking the feature.
g. Contextual code completion must be highly accurate. The engine must avoid attempting to provide completions inappropriately, resolving the completion bug with strings and ensuring completions work correctly with file names.
h. Mouse-based navigation must be intuitive and precise. A double-click action must accurately select a valid python identifier, and deliberately not trigger standard selection behavior when double-clicking inside comments or strings. Furthermore, utilizing Control-Click on a function must instantly hyperlink the user to the function's definition without raising an exception.

**Execution, Orchestration, and Debugging**
i. Aptana Studio shall act as a robust control center for application execution. The IDE must cleanly orchestrate process creation, preventing the 'Error Creating Python Process' message that currently blocks execution. Crucially, the process lifecycle must be tied to the IDE; the architecture must guarantee that a spawned python process does not survive to the operating system level after Eclipse has been closed or the debug session terminated.
j. The debugging suite must provide granular control over execution flow. The debugger must reliably start with a breakpoint already set, rather than ignoring early breakpoints.
k. Stepping logic must be flawless. The debugger must implement the ability to reliably "Step into" functions, and ensure the Stepping icons within the Eclipse toolbar are not erroneously disabled during an active session. Additionally, the Location arrow visibility must be maintained so the developer always knows which line is currently executing.
l. Advanced exception handling must be integrated. The engineering team must implement a "break for exception" feature, allowing the debugger to automatically halt execution the moment an unhandled exception is thrown.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, and the complex cross-platform execution requirements necessary for an Eclipse-based IDE.

### 3.1 Reliability of the framework

Reliability of the local development environment is absolutely paramount; an unstable IDE destroys developer momentum and leads to catastrophic data loss. The system must guarantee operational stability across highly volatile local workspaces.

The most severe reliability defects must be addressed immediately as blockers for release. The system must fix the critical defect where Eclipse simply closes on save, resulting in lost work. Furthermore, the editor hanging on version 0.6.1 must be diagnosed and resolved, as blocking the main UI thread renders the tool completely unusable.

Compatibility with the underlying Eclipse Rich Client Platform is a strict mandate. The editor currently fails to load on Eclipse 3.0 M5, is not working in 3.0M6, and version 0.4.1 does not run in Eclipse M9. The plugin initialization sequence must be refactored to ensure broad compatibility across these Eclipse milestone releases. Additionally, the system must fix the regression where users cannot launch any `*.py` files in Eclipse 3.0.

File handling must be completely deterministic. Currently, `OpenExternalFile` fails in Eclipse 3.0, and external files are incorrectly opened in read-only mode. The IDE must properly negotiate file locks with the host operating system to allow seamless editing of files outside the immediate workspace.

### 3.2 Information volume and computational overhead

The system should be extremely efficient, as it shares workstation resources with heavy native runtimes and local web servers. To accurately manage its footprint, the Studio's internal indexer must intelligently cache project metadata.

During runtime execution, the system must carefully manage standard input and output streams. A defect exists where the `raw_input` command leaves a `\r` carriage return at the end of the string, corrupting data input processing during debug sessions. The console streams must be scrubbed and normalized across operating systems to prevent these parsing errors.

Furthermore, the syntax validation engine must be mathematically accurate. The parser currently reports a syntax error incorrectly when encountering the `yield 3` generator expression; the AST grammar must be updated to support the full scope of the language specification.

### 3.3 Developer interface

The Graphical User Interface (GUI) must be intuitive, predictable, and aligned with standard IDE paradigms. Visual indicators are critical for developer orientation. The engineering team must fix the wrong icon being displayed for specific file types or run configurations, ensuring visual consistency throughout the Project Explorer.

Configuration interfaces must be highly reliable. The Debug Preferences menu is currently documented as "broken," which prevents developers from configuring timeouts and port allocations; this UI must be entirely reconstructed to ensure settings persist correctly. Additionally, a missing `timeout not defined` exception must be handled gracefully within the preference loading sequence.

The update mechanism must provide accurate feedback. Currently, the scan for updates keeps sending version "0.3" to the update server regardless of the actual installed version. Furthermore, the Discovery site URL configured within the update manager is wrong and must be repointed to the correct production server.

### 3.4 User characteristics

The intended users of Aptana Studio are highly technical web developers, backend scripting engineers, and full-stack software architects. They are typically writing code in dynamic scripting languages and rely heavily on the IDE to abstract away the complexity of process management and remote debugging. They require an environment that feels fast and responsive, demanding that features like code completion and syntax highlighting operate instantaneously without interrupting their typing flow.

### 3.5 Programming language constraints

The primary programming language utilized for the underlying execution engine of the IDE itself is Java, due to its foundation on the Eclipse Rich Client Platform. This mandates strict adherence to OSGi bundle architectures and Eclipse plugin manifests.

However, the Studio must also bridge into other language environments flawlessly. Because the tooling heavily inspects dynamic scripts, the socket communication between the Java frontend and the language-specific backend parsers must be robust and secure. Data serialized over this Code Completion socket must be strictly formatted to prevent buffer overflows or parsing exceptions.

### 3.6 Process requirements

As an enterprise-grade tooling product, rigorous organizational testing and distribution processes must be fulfilled. The product's value proposition relies entirely on its ability to function uniformly across different operating systems.

The QA process must heavily emphasize cross-platform validation. The issue tracker specifically highlights that completion fails under Linux for 0.6, code completion fails under Mac OS X for 0.6, there are general problems with 0.6.0 on Linux, and there is a need for Code Completion Under XP clarification. The release engineering team must implement an automated matrix testing strategy that guarantees core features like sockets, process creation, and text editing are verified simultaneously on Windows XP, macOS, and Linux prior to any public release.