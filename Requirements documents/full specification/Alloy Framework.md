# Alloy Framework

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Alloy Framework and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and compilation
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive requirements of a system designed to assist the global mobile development community, specifically those engineers and organizations utilizing the Appcelerator Titanium Software Development Kit (SDK). The system will provide a standardized, robust architecture to analyze, structure, compile, and execute mobile applications across multiple disparate operating systems from a single unified codebase.

### 1.1 The Project at a Glance

The software to be produced will be named *Alloy Framework*, and will be referred to as Alloy in the rest of this document.

The main purpose of Alloy is to provide an Apache-licensed model-view-controller (MVC) application framework built on top of Titanium that provides a simple model for separating the application user interface, business logic and data models.


The client development community currently utilizes standard, imperative Titanium API calls that are used for this purpose. However, the age of this methodology and its inherent design inadequacies become evident as the application codebase size and query complexity increase. The current standard often results in deeply intertwined code where presentation logic and business rules are conflated within the same JavaScript files, leading to high maintenance costs and an increased likelihood of memory leaks. It is now obvious that the standard method of imperative UI generation will be obsolete relatively soon, and the Alloy framework will therefore phase out the previous system.

The high-level goals of the new system are:
a. To radically reduce the time and complexity required for developers to produce application interfaces by allowing the user to have JavaScript and CSS in separate files to maintain presentation logic separation. This structural division ensures that developers can modify the visual appearance of an application without inadvertently altering its underlying behavioral logic.
b. To increase developer confidence and adoption by presenting real value in terms of productivity; specifically, the framework must be prepared to clearly explain to users why it has chosen HTML and CSS styling paradigms versus XML and JSON configurations, demonstrating that the chosen approach offers superior productivity compared to other techniques.
c. To reduce the repetitive and error-prone boilerplate code required to generate cross-platform elements by allowing the user to use namespaces like iPhone, Mobile Web and Android to create UI elements, deprecating the current standard of manually prepending `Ti.UI.createX` for every single object instantiation.
d. To accelerate enterprise application development by providing a new, comprehensive set of modular components that allows the user to use several pre-packaged widgets to create apps.
e. To ensure complete interoperability with existing Appcelerator enterprise tooling by ensuring all node processes required to support the ZipTi build system are public, so that outside processes like Ti Studio can find and run them without friction.
f. To provide the community with highly reliable reference materials by supplying a couple of full functioning Appcelerator apps that include widgets, look awesome, demonstrate best practices, and run seamlessly across platforms.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the framework's implementation:

* *Alloy* – The MVC application framework this document is concerned with, which is built to run as an abstraction layer on top of the Appcelerator Titanium SDK.
* *CommonJS* – A project with the goal of specifying an ecosystem for JavaScript outside the browser. Alloy will rely heavily on CommonJS `require()` module patterns to manage scope and dependency injection.
* *Declarative UI* – A paradigm of user interface design where the developer describes *what* the UI should look like (using markup) rather than writing the step-by-step imperative programming commands to construct it.
* *Node.js* – The asynchronous event-driven JavaScript runtime that will power the command-line compilation tools, parsers, and the ZipTi build scripts for the framework.
* *Sizzle* – A pure-JavaScript CSS selector engine that will be directly integrated into ZipTi via commonjs to ensure that the internal architecture can reliably retrieve the correct dom elements during the translation phase.
* *Ti Studio* – An external, Eclipse-based Integrated Development Environment (IDE) process developed by Appcelerator. Ti Studio needs to be able to find and run node processes and grab widgets via a public interface to provide GUI-based tools for Alloy.
* *Widget Factory* – A standardized system design based on W3C specs that can handle unique ids, nested widgets, and css for class and ids to ensure isolated component generation.
* *ZipTi* – The underlying node-based build system and compilation pipeline associated with the framework that requires comprehensive logging and a dedicated system for testing HTML/CSS grammars.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the parsing, compilation, and runtime environments. Section 3 mentions other necessary considerations, including performance constraints, developer interfaces, and programming language dependencies.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the compiler and runtime must behave.

### 2.1 Alloy Framework and its environment.

The following description outlines the intended relationship between Alloy, the developer's local machine, and its surrounding compilation environment:

* Developer source code (consisting of declarative markup, styling files, and business logic scripts) flows from the developer's local development environment to the node-based compiler scripts. These translator and package scripts must be rigorously modified to be node NPM compliant.
* During the compilation phase, processed scripts and styles are scanned by the system and appended to the final CSS and script source files.
* To maintain a clean project structure that does not interfere with the developer's source files, all generated files are automatically moved to a "generated" folder inside the project's standard Resources folder.
* The Titanium Studio IDE acts as an outside process that interacts with the framework's public interfaces and widgets, requiring a predictable directory structure and exposed executable commands.

The main inputs to Alloy come from the developers writing the application. It is the job of the system and its compiler to thoroughly analyze and process the files, resolve all styling and widget dependencies, generate standard, highly-optimized Titanium JavaScript based on them, and deliver the compiled output to the Titanium SDK for final native rendering on the targeted devices.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the framework:

**Declarative UI and View Generation**
a. The Alloy Framework shall provide an interface to completely separate presentation logic from business logic. The user wants to use CSS and style by id, class and style attribute. To facilitate this, the framework's compiler must parse these styling rules and merge the class, id and style css into a single css rule.
b. The system must ensure that complex markup can be accurately parsed. The framework will integrate the Sizzle engine into Zipti via commonjs to ensure that complex dom structures can be added and the selector engine can reliably retrieve the correct dom elements at compile-time and runtime.
c. The framework must guarantee that developers can define complex UI properties. Currently, there's no way to specify complex types in markup for UI properties; the system must be updated to support passing complex JSON objects and arrays directly through the declarative markup. Furthermore, developers currently can't create DOM elements without an ID; this limitation must be removed to allow anonymous elements.
d. The framework must support dynamic styles like fonts that become json objects, requiring the development of a method that can map from css directly to the native Ti API equivalents. For styles that fall outside this scope, the team must work with internal stakeholders (like Arthur) and document exactly how they should be done in code.
e. During the translation process, the framework must ensure that the translated markup has the relevant css and script included properly. Furthermore, the system must handle using combined css to apply the style immediately during object creation, preventing visual layout jumping on the device.

**Platform-Specific Compilation**
f. The Alloy Framework shall provide the capability of obtaining platform-specific UI rendering without requiring the developer to write branching `if/else` JavaScript logic. The framework will add a new markup attribute called `data-ti-platform="iPhone,iPad"`.
g. The compiler will take the `data-ti-platform` attribute and, during code generation, automatically put an `if ([platform])` statement around the element in the generated JavaScript. Crucially, to save memory and parsing time, the compiler must entirely ignore subelements of that node if the current build target does not match the specified platform.

**Widget Architecture and Reusability**
h. The Alloy Framework shall provide a robust widget architecture to promote code reuse. The user wants to create elements and widgets and be able to extend and wrap existing Ti API so that native proxy issues can be avoided entirely.
i. These widgets need a specific, standardized directory structure and a public interface so they can be easily grabbed by outside processes like Ti Studio.
j. The system shall implement a Widget Factory based heavily on W3C specs that can elegantly handle unique ids, deeply nested widgets, and encapsulated css for class and ids without style bleed between components.
k. The framework shall provide several pre-packaged widgets to create apps, ensuring that common UI paradigms do not need to be rebuilt from scratch by every developer.

**Runtime API and DOM Manipulation**
l. The Alloy Framework shall implement a jQuery-like syntax for post-creation UI manipulation. The system will create the `$Ti(selector).css(x)` method for returning a property and `$Ti(selector).css(x, y)` for dynamically setting values at runtime.
m. The framework shall provide comprehensive, platform-agnostic logging capabilities. The framework will add warning and error debugging to a unified `$Ti.Logger` object. To prevent application thread blocking, the Logger itself should just queue messages and later be queried for its content, ensuring that logging behaves in a platform-independent way.
n. The runtime environment must be hardened against failure. Previously, the `runtime.js` file was throwing exceptions on the Android emulator; this must be isolated and fixed to ensure cross-platform parity. Furthermore, the system must be patched because the previous xpath removal broke the runtime completely.

**Compilation, Parsing, and File Handling**
o. The framework must support both network and local file compilation robustly. Currently, the system just goes through metadata files; it needs to be updated to actively open external script and css files within `ti_ui_translator.js`, handling both local and network-based files seamlessly.
p. The build system must be able to gracefully handle JSON definitions. The architecture team must evaluate if files like `json.pegjs` and `json.js` are actually necessary for the final build pipeline, or if native JSON parsing can be utilized. Furthermore, the system must allow developers to use constants for JSON properties to improve code maintainability.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, reliability mandates, and developer experience requirements.

### 3.1 Reliability of the framework

Reliability of the compiler and the resulting runtime code has a critical priority. The system must guarantee total accuracy in translating the markup. To achieve this, a system for testing HTML and CSS grammars needs to be a part of the ZipTi build system to ensure grammars are absolutely correct before finding parser errors later in the build chain.

When parser errors do occur, or when runtime issues happen, the system must significantly improve runtime error messages to rapidly aid developers in debugging their applications. Furthermore, ZipTi will need highly comprehensive logging to trace the exact steps taken during the generation of the `Resources` directory.

To ensure absolute stability across different developer environments, the engineering team must make sure to rigorously test node scripts on Linux and Windows operating systems, not just macOS. The DOM parsing mechanisms, which were previously noted as "busted", must be completely overhauled and stabilized with comprehensive unit tests.

### 3.2 Information volume and compilation

The system should be able to compile massive enterprise applications efficiently, and the runtime must not suffer from slow initialization. A critical performance bottleneck must be addressed: the `eval()` of DOM scripts at app startup was increasing initial load time significantly.

To solve this memory and performance constraint, the framework must systematically replace the `eval()` of runtime W3C libraries with strict CommonJS `require()` calls. However, the engineering team must be careful, as the current `require()` scheme fails on the Mobileweb platform target; this platform discrepancy must be resolved prior to release.

Furthermore, to handle large volumes of declarative UI code, the system must radically improve HTML parsing performance. The architecture team should actively consider using `jsdom` for HTML parsing and DOM creation during the build phase if the current custom parser cannot meet the sub-second compilation requirements. The CSS runtime parsing also needs to be entirely revised to ensure it does not block the main execution thread on lower-end Android and iOS devices.

### 3.3 Developer interface

The community expressed repeatedly that the developer interface and onboarding experience of the system should be a major priority. The user wants to have high-quality, pre-release docs that explicitly explain how to install and use the Declarative UI.

The installation process must be frictionless. The user would like to run the Declarative UI translator but strictly does not want to do a custom, complex install of secondary components. The framework should ideally be a single NPM global install. Furthermore, it is required that any utility scripts that operate on ZipTI can be executed smoothly from both the terminal command-line or triggered via the graphical Ti Studio interface.

### 3.4 User characteristics

The intended users of Alloy are a vast subset of the global Appcelerator developer community. They are typically web developers transitioning into mobile development, which is why matching W3C specs and utilizing CSS/HTML paradigms is so critical for the framework's adoption. They require a framework that handles complex native SDK integrations seamlessly behind a friendly, web-like abstraction.

### 3.5 Programming language constraints

The programming language to be used for the underlying compiler relies entirely on Node.js and strict adherence to CommonJS standards. To ensure full compatibility with modern Node environments, the runtime must replace the outdated use of 'exports' with the standard 'module.exports' in the `runtime.js` file.

Additionally, the framework must use commonjs to execute the `app_dom.js` file. All build tools, plugins, and CLI commands must be written in JavaScript and must be fully NPM compliant to integrate with the broader open-source JavaScript ecosystem.

### 3.6 Process requirements

Once the core Appcelerator team and the open-source community agree on feature figures for the software, the project leader will ensure proper software testing protocols are strictly followed. To prevent regressions in future versions of the compiler, the team must mandate the creation of complex source code to test the proper operations of the generated parsers. Only when these comprehensive parser tests pass locally will pull requests be accepted into the master repository.