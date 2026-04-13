# Appcelerator Command-Line Interface

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Appcelerator Command-Line Interface and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and compilation overhead
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document delineates the comprehensive software requirements, architectural specifications, and strategic performance targets for the initial instantiation of a highly scalable, unified Command-Line Interface (CLI). This system is engineered from the ground up to provide a centralized, secure, and highly extensible command-line environment for enterprise mobile developers. The tool will serve as the primary gateway for developers to check and configure their environment setup, create new application scaffolds, and orchestrate complex build pipelines across multiple mobile operating systems.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named the *Appcelerator Command-Line Interface*, and will be referred to as the Appc CLI or "the system" in the rest of this document.

The primary purpose of the Appcelerator Command-Line Interface is to act as the foundational entry point for the entire Appcelerator ecosystem. Modern mobile software development suffers from profound tooling fragmentation; developers are routinely forced to juggle distinct scripts for iOS compilation, Android packaging, cloud service deployment, and environment validation. The Appc CLI aims to establish a unified, democratized, and highly structured terminal workspace where developers can execute all tasks through a single, cohesive `appc` binary.

The high-level goals of this new platform instantiation are:
a. To radically simplify application lifecycle management by providing a suite of unified commands—such as a dedicated `appc test` command—to establish a standardized testing and execution pipeline for all Titanium and Arrow applications.
b. To ensure uncompromising reliability for mobile developers operating in restricted network environments, specifically requiring that the architecture allows local compilation to succeed unconditionally; the system must guarantee that a build to iOS simulator or a build to Android does not fail when offline.
c. To establish a highly secure and intelligent session management protocol. The system must automatically prompt for a new login when a session is invalid, while ensuring that the platform website and CLI do not inadvertently invalidate each other's session tokens.
d. To provide enterprise-grade environment validation and configuration, allowing users to effortlessly check their system dependencies (Node.js, Android SDKs, Xcode) via an `appc setup` command, ensuring that cross-platform prerequisites are met prior to compilation.
e. To significantly streamline multi-platform mobile builds by eliminating architectural bottlenecks, ensuring that developers can rapidly build a Titanium project to both the iOS simulator and Android emulator concurrently without cross-contamination of build artifacts.
f. To integrate seamlessly with graphical Integrated Development Environments (IDEs), specifically ensuring that updating the `tiapp.xml` file in Appcelerator Studio dynamically reflects the update on the centralized Cloud Dashboard via the CLI's background synchronization mechanisms.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the command-line interface's implementation:

* *ACS* – Appcelerator Cloud Services. The backend-as-a-service platform. The CLI must integrate with ACS, ensuring that commands like `appc acs` and `appc cloud` reference the exact same, synchronized versions of the underlying ACS CLI binaries to prevent version mismatch errors.
* *appc* – The primary terminal executable name for the Appcelerator Command-Line Interface.
* *Arrow* – Appcelerator's API building framework. The CLI must natively support the scaffolding, testing, and publishing of Arrow apps on Windows, macOS, and Linux.
* *encryptJS* – A proprietary security mechanism used to obfuscate JavaScript source code during the build process. The architecture must account for encryptJS forcing a full rebuild of the Titanium application to ensure security constraints are met.
* *io.js* – A JavaScript platform built on V8, which temporarily diverged from Node.js. The CLI must maintain strict runtime compatibility, ensuring that users are never unable to run `appc setup` on io.js environments.
* *NPM* – Node Package Manager. The default package manager for the JavaScript runtime environment. The CLI relies heavily on NPM for its internal plugin architecture.
* *tiapp.xml* – The core configuration file for Titanium applications, dictating SDK versions, module dependencies, and application metadata.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the project creation routines, the build and execution pipelines, and the cloud synchronization adapters. Section 3 mentions other necessary considerations, including strict performance constraints, developer interface (UX) requirements, security and authentication mandates, and the process requirements for updating the CLI itself.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core Node.js engine, the local compilation adapters, the authentication prompts, and the configuration managers must behave during standard operation and under heavy enterprise development load.

### 2.1 Appcelerator Command-Line Interface and its environment.

The following description outlines the intended relationship between the Appc CLI, the developer's local operating system, the native mobile SDKs, and the external Appcelerator Cloud platform:

* Developer commands flow from the system terminal (Bash, Zsh, Windows Command Prompt) directly into the `appc` Node.js binary, which parses the arguments and routes the request to the appropriate internal sub-module.
* To support massive enterprise rollouts, the architecture must support robust proxy interactions. It is a foundational requirement to add proxy logic to the underlying appc processes, such as the ACS uploading utilities, to ensure corporate firewalls do not block developer operations.
* The CLI must constantly manage its own configuration state. Developers must be able to add and configure settings, and conversely, the system must ensure that users are never in a state where they cannot remove settings from the `appc config` file.
* When users require native compilation, the CLI acts as an orchestrator, invoking Xcode command-line tools (`xcodebuild`) or the Android SDK (`dx`, `aapt`) to compile the JavaScript payload into native binaries.
* The system must communicate flawlessly with the Appcelerator API gateway. In the event of network disruption, the CLI must gracefully handle gateway timeout error 504 responses without crashing the local Node process.

The main inputs to the Appc CLI come from developers typing commands, passing execution flags, and authenticating via standard input prompts. It is the job of the system's execution engine to continuously analyze these inputs, manage local session states, generate dynamic build configurations, and deliver the compiled application to the requested emulator, simulator, or tethered device seamlessly.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the mobile development framework:

**Project Creation and Configuration**
a. The Appc CLI shall provide an industry-leading, highly expressive scaffolding engine. The `appc new` command must be streamlined; the architecture team is required to clean up `appc new` arguments to ensure the user experience is intuitive and free of redundant parameters.
b. The system must support advanced modular development. The creation engine must allow Titanium modules to be created using the `-t` flag (e.g., `-t module`), providing a distinct scaffolding pipeline separate from standard applications.
c. Data integrity during project creation is paramount. The system must ensure that passed in options are strictly respected during project creation, preventing scenarios where user-defined IDs or names are overwritten by defaults. Furthermore, the system must add a strict validation restriction that the application name field cannot start with a number, which violates native iOS and Android compilation rules.

**Build, Execution, and Deployment Pipelines**
d. The Appc CLI shall serve as the ultimate build orchestrator. The `appc run` command must be exceptionally stable. The architecture must prevent states where `appc run` fails to execute due to unhandled promise rejections, and specifically ensure that `appc run` does not fail for Titanium projects if prompting occurs during the execution flow.

e. Cross-platform build continuity must be guaranteed. The compilation engine must maintain isolated build states to ensure that executing a build to an iOS device and then immediately to an iOS simulator never fails due to cached artifact conflicts. Similarly, rebuilding an application for the Android emulator must execute flawlessly on subsequent runs.
f. To prevent stale code from ruining a debug session, the build pipeline must automatically wipe native module folders before compiling, ensuring a pristine integration of third-party native code.
g. The system must intelligently guide the developer during compilation. If the underlying Android build tools detect an environment mismatch, the CLI must generate an Android build tool warning that explicitly directs the user to run "ti config" to resolve their local paths.
h. Cloud deployment commands must be highly configurable. The `appc unpublish` command must explicitly support the `--project-dir` flag to allow CI/CD servers to unpublish applications without needing to navigate the shell into the target directory.

**Authentication, Session, and Security Management**
i. The platform must provide robust and frictionless identity management. The architecture requires that certain passthrough commands, such as "clean", be explicitly added to a whitelist of commands that need not prompt for authentication, allowing developers to wipe their build directories while offline or logged out.
j. Interactive prompts must be intelligent. The system must resolve the architectural defect where passing in `--org-id` to certain commands when logged out still prompts the user to select an organization; the CLI must respect the provided flag and automatically route the authentication request. Furthermore, the system must prevent the CLI from prompting for login twice when the `--env` option is given in the command.

k. Permissions must be validated client-side to save time. If a developer's account is unable to perform actions such as `package`, the system must ensure that when attempting to package, the command exits immediately with an unauthorized error rather than executing a 10-minute build only to fail at the upload stage. Similarly, the system must actively alert users when attempting to run an app that belongs to a different org than they are currently logged in as.
l. Device authorization lifecycle must be manageable via the CLI. The system must ensure that the `-D` option utilized with `appc logout` successfully deauthorizes the specific local device from the Appcelerator platform.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, the complex data presentation policies, and the upgrade requirements necessary for a globally distributed developer tool.

### 3.1 Reliability of the framework

Reliability of the Node.js application layer, the network connections, and the resulting native artifacts has a critical priority. The CLI is the developer's primary interaction point; if it hangs or crashes, all development halts.

The system must guarantee operational stability and security. The network communication layer must be fortified against SSL man-in-the-middle attacks. However, the system must gracefully handle certificate rotations; the architecture must automatically update `appc-request-ssl` on a fingerprint failure. If an unauthorized proxy is detected, the system must clearly output that the "Servername" is not authorized for SSL due to a mismatched SSL fingerprint, securely halting the operation.

The runtime engine must handle unexpected states securely. The architecture must resolve edge cases such as a "Security Violation in iOS Simulator" occurring during application injection. Furthermore, developers often require elevated testing contexts, but the CLI must defensively disable Rooted Phone detection by default to prevent the tooling from artificially blocking deployment to legitimate developer test devices.

Process termination must be clean. A critical developer experience requirement dictates that "ctrl+c" must kill the Appc CLI gracefully when a user tries to log in, restoring the terminal state and cursor visibility without leaving orphan Node processes running in the background.

### 3.2 Information volume and compilation overhead

The system must be engineered to manage the execution of massive enterprise application builds, which include hundreds of megabytes of image assets, JavaScript files, and native libraries.

To guarantee this level of performance and consistency at scale, the dependencies of the CLI itself must be strictly managed. The infrastructure team must investigate locking down NPM dependencies using shrinkwrap or package-lock mechanisms, ensuring that every developer globally downloads the exact same dependency tree, preventing "works on my machine" anomalies.

When executing internal updates, the system must prevent file locks and volume corruption. The architecture must gracefully handle and prevent random "Cannot find module" errors when updating via the "appc use latest" command, ensuring the npm installation completes fully before the new binary is invoked.

Configuration variables must be parsed correctly regardless of volume or type. The `appc-security` properties subsystem must be rigorously refactored to properly handle `bool` values (true/false) instead of interpreting everything as strings, which currently breaks downstream compilation logic.

### 3.3 Developer interface

The community of mobile developers requires extensive, predictable, and highly legible terminal interfaces. The nomenclature and output used by the CLI must be intuitive.

Error handling must be exceptional. When the backend infrastructure is unavailable, the CLI must provide better error messages when the server is down, rather than dumping raw socket exceptions to the terminal. Specifically, the `appc login` command must be patched so it does not return raw HTML content (like an Nginx 502 page) when the server is not responding; it must parse the failure and present a localized, color-coded error string. Similarly, if a user enters an incorrect password for enabling the Test service, the system must ensure there is an immediate error or re-prompt, resolving the silent failure state. The login validation error message must always be successfully passed through the prompt from the CLI to the user.

When querying for system information, the output must be strictly formatted. The architecture team must ensure that when no SDKs are installed, running `appc ti sdk -o json` does not return unparseable error text, but instead returns a valid, empty JSON array so that CI/CD servers can parse the response without crashing.

Versioning information must be crystal clear. The system must ensure that running `appc ti -v` correctly returns the Appc CLI version (or the wrapped Titanium CLI version), ensuring developers can accurately report bugs.

### 3.4 User characteristics

The intended users of the Appcelerator Command-Line Interface span from highly technical native mobile engineers to frontend web developers migrating into the mobile space. They require a framework that handles complex native SDK integrations (like Android NDKs and iOS Provisioning Profiles) seamlessly behind a friendly, highly expressive text-based layer. The user experience must be frictionless; functions like logging in, generating certificates, or launching an emulator must be achievable with simple, memorable commands. They operate in highly variable network conditions (coffee shops, airplanes, corporate VPNs), making the requirement for offline compilation and robust proxy support absolutely essential.

### 3.5 Programming language constraints

The primary programming language utilized for the underlying execution engine of the CLI itself is JavaScript, executing within the Node.js runtime environment. This mandates strict adherence to asynchronous programming architectures, non-blocking I/O, and robust promise management.

The parsing engine must be meticulously compatible across different Node.js and OS versions. The development team must immediately patch the core parser to prevent the fatal "Unexpected token W" exception from occurring during `appc setup`, which indicates a failure to parse malformed JSON or binary streams returned by the operating system.

### 3.6 Process requirements

As an enterprise-grade developer tool, rigorous organizational testing, deployment, and update processes must be fulfilled. The product's value proposition relies entirely on its ability to maintain seamless integration with the broader Appcelerator ecosystem.

The lifecycle of the CLI itself must be manageable. A dedicated initiative is required for generally improving CLI updates, ensuring that users can transition between major versions without corrupting their global npm environment. To support safe installations, the deployment script must only set the active version flag after the installation has completely and successfully finished, preventing the system from pointing to a half-downloaded binary.

Finally, the CLI must cooperate safely with desktop applications. The installation and update routines must implement file-locking awareness to prevent errors updating the Core CLI when Appcelerator Studio is actively open and holding locks on shared configuration files. Furthermore, the unified identity model must be hardened to ensure developers can not find themselves in a state where they can not login in Appcelerator Studio due to a corrupted CLI session token. Every action must prioritize developer productivity, deterministic behavior, and rock-solid reliability.