# Appcelerator Daemon

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Appcelerator Daemon and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and computational overhead
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive software requirements, architectural specifications, and strategic performance targets for a highly integrated background service designed to accelerate mobile and cross-platform application development. This system is engineered to run persistently on a developer's local workstation, providing a unified, high-speed services layer that powers complex compilation tooling, platform detection, and device management without the overhead of repeatedly bootstrapping command-line environments.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *Appcelerator Daemon* (frequently referred to by its executable name, `appcd`), and will be referred to as the Daemon in the rest of this document.

The primary purpose of the Appcelerator Daemon is to act as a persistent server that runs on a developer's computer and hosts services which power the tooling for Axway products such as the Axway Titanium SDK. The client development community currently utilizes traditional, transient Command Line Interfaces (CLIs) to trigger builds, detect connected devices, and compile assets. This legacy methodology requires the Node.js runtime and massive dependency trees to be fully loaded into memory from scratch upon every single command invocation, resulting in severe latency and degraded developer productivity. The Appcelerator Daemon v1 aims to completely phase out this redundant bootstrapping effort by keeping the core compilation engines, file watchers, and platform detection libraries constantly warm and accessible in the background via local HTTP and WebSocket protocols.

The high-level goals of the new daemonized architecture are:
a. To radically reduce application build times by maintaining long-lived processes that handle repetitive tasks, such as executing the Titanium Android, iOS, Windows, and Mobile Web build implementations.
b. To establish a highly modular, extensible ecosystem by integrating a dynamic hook system and implementing a comprehensive plugin manager directly into the `appcd` core.
c. To provide robust, real-time communication between the developer's IDE (like Titanium Studio) and the underlying build tools by allowing for multiple asynchronous requests over the exact same WebSocket connection.
d. To ensure flawless integration with the broader Axway cloud ecosystem by providing an `@appcd/plugin-amplify` plugin that serves as the centralized Authentication service and AMPLIFY platform daemon plugin for the local machine.
e. To significantly improve cross-platform environment detection—locating SDKs, emulators, and connected hardware—by deploying the next generation of detection libraries, specifically `ioslib 2.0`, `androidlib v2`, `windowslib v2`, and `jdklib v2`.
f. To provide advanced, real-time development capabilities by deeply integrating Alloy 1.next and LiveView 2.0 directly into the daemon's service layer, allowing for hot-reloading of application assets on connected devices.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the background daemon's implementation:

* *appcd* – The standard abbreviation and command-line executable name for the Appcelerator Daemon.
* *Alloy* – The declarative model-view-controller (MVC) framework built on top of Titanium. The daemon must integrate tightly with Alloy 1.next to process view and style compilations efficiently.
* *AMPLIFY* – Axway's enterprise integration and API management platform. The daemon acts as the local bridge to this cloud environment via the `@appcd/plugin-amplify` module.
* *Gulp* – A cross-platform, streaming task runner that lets developers automate many development tasks. The daemon's internal build system utilizes a top-level gulp file to create its package distributions.
* *Koa* – A modern, lightweight web framework designed by the team behind Express. The `appcd-dispatcher` module requires the addition of a Koa middleware function to cleanly route incoming HTTP and WebSocket requests.
* *LiveView* – A development tool that allows for real-time, instantaneous updates to a running mobile application without requiring a full recompilation cycle. LiveView 2.0 services will be hosted within the daemon.
* *node-pre-gyp* – A tool used to publish and install Node.js C++ addons from binaries. The daemon relies on this to install native bindings, specifically for the `node-ios-device` module.
* *Titanium SDK* – The core open-source framework that allows the creation of native mobile apps from a single JavaScript codebase. The daemon provides specialized services for TiSDK specific tooling.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the HTTP/WebSocket dispatchers, the extensible plugin architecture, and the specific mobile build backends. Section 3 mentions other necessary considerations, including strict platform compatibility, local developer interfaces, Node.js packaging constraints, and continuous integration methodologies required to maintain the stability of the tooling.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core daemon process, the dynamic plugin manager, and the mobile compilation pipelines must behave during operation.

### 2.1 Appcelerator Daemon and its environment.

The following description outlines the intended relationship between the Appcelerator Daemon, the local developer's operating system environment, and external IDE clients:

* The Appcelerator Daemon launches as a background service on macOS, Windows, or Linux workstations. It binds to a local port to listen for incoming tooling requests.
* Integrated Development Environments (IDEs), text editors, or CLI tools send configuration and build commands to the daemon via HTTP POST requests or persistent WebSocket connections.
* The daemon's internal `appcd-dispatcher` routes these requests through Koa middleware to the appropriate loaded plugin (e.g., routing an iOS build request to the `@appcd/plugin-titanium` module).
* The daemon relies on a highly sophisticated filesystem watcher to monitor the developer's project directory for source code changes, instantly triggering LiveView updates or re-compilations.
* The daemon periodically connects to external Axway servers to validate Amplify authentication tokens and transmit anonymized telemetry and analytics events.

The main inputs to the Appcelerator Daemon come from developer tooling issuing compilation or environment-query commands. It is the job of the system's core dispatcher to continuously analyze and process these requests, validate the JSON payloads, invoke the heavy C++ or Java build systems asynchronously, and stream the build logs back to the requesting client without blocking the Node.js event loop.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the background tooling framework:

**Core Daemon Server and Dispatcher**
a. The Appcelerator Daemon shall provide a highly robust, non-blocking local web server. The architecture team must port the `appcd-http` implementation from its initial prototype into the production core. This HTTP server must allow administrators to configure a default served root directory for hosting local assets.
b. The system must support advanced payload manipulation. To optimize local network traffic and client-side parsing, the daemon must implement robust JSON response filtering directly within the core dispatcher.
c. The network layer must support complex, concurrent operations. The daemon shall allow for multiple requests over the exact same WebSocket connection, implementing a multiplexing protocol so that a developer can simultaneously stream device logs, compile a project, and query system stats without opening redundant TCP sockets.
d. The incoming request pipeline must be standardized. The `appcd-dispatcher` module must add a Koa middleware function to seamlessly handle standard HTTP semantics and RESTful routing.
e. Global configuration and localization must be supported natively. The architecture must introduce an `appcd-response` module that adds a comprehensive i18n (internationalization) system to ensure error messages and build statuses can be localized for the global development community.

**Plugin Management and Hook System**
f. The Daemon shall not be a monolith; it must provide an architecture based on dynamic extensibility. The engineering team must implement a robust plugin manager within the `appcd-plugin` module that can dynamically discover, load, and manage the lifecycle of external tooling packages.
g. The system must provide a deep event-driven architecture. Developers are required to integrate a hook system into the appc daemon core, allowing plugins to intercept and mutate the behavior of other plugins or core services.
h. The framework must natively support a System Info appc daemon plugin, which securely exposes local machine capabilities (CPU architecture, memory, OS version) to the requesting tooling to optimize build thread allocation.

**Titanium and Amplify Integrations**
i. The system must replicate and enhance all legacy SDK capabilities. The team must construct the `@appcd/plugin-titanium` package, which will explicitly contain the Ti project service, the legacy Ti build system wrappers, and all necessary services for TiSDK specific tooling.
j. The framework must support the full suite of mobile and desktop compilation targets. Within the Titanium plugin, the daemon must provide the dedicated Titanium Android build implementation, the Titanium iOS build implementation, the Titanium Windows build backend, and the Titanium Mobile Web build backend.
k. Enterprise authentication must be managed centrally. The team must develop the `@appcd/plugin-amplify` package to act as the official Authentication service, ensuring developers only need to log in once per machine rather than per terminal session.

**Environment Detection Libraries**
l. The Daemon shall rely on a new suite of hardened, asynchronous detection libraries to map the host environment. The system will deploy `ioslib 2.0` specifically optimized for environment detection (locating Xcode installations, iOS simulators, and provision profiles).
m. Similarly, the system must deploy `androidlib v2` to parse the complex Android SDK directory structures and locate connected hardware via ADB.
n. To support cross-platform parity, the daemon must also deploy `windowslib v2` (for detecting Visual Studio and MSBuild) and `jdklib v2` (for locating valid Java Development Kit paths required by the Android compiler).

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, and the complex cross-platform installation requirements.

### 3.1 Reliability of the framework

Reliability of the background daemon is arguably its most critical feature; a crashing daemon halts all local developer productivity. The system must guarantee operational stability across highly volatile local environments.

Specifically, the detection libraries must handle edge cases gracefully. On Windows environments, if a user decides to move their JDK while running the `jdklib.watch()` function, the system currently throws a fatal `TypeError: Path must be a string` error; this state must be caught and gracefully handled to simply report a missing JDK instead of crashing the daemon.
Similarly, within `androidlib v2`, if a developer calls `androidlib.detect()`, the system must ensure it does not crash, fixing the bug where an empty array is incorrectly returned for the results. Furthermore, calling `androidlib.watch()` currently throws a fatal `TypeError: _nodeAppc2.default.detect.Watcher is not a function`, which must be immediately remediated.

Native C++ bindings are historically fragile. To prevent catastrophic failure when interfacing with Apple hardware, the `node-ios-device` module must automatically re-run `node-pre-gyp` if the necessary native binding doesn't exist on the local filesystem, guaranteeing a successful fallback compilation.

Finally, the filesystem watcher utilized by the daemon is currently unreliable in complex workspace setups. The `node-appc` fs watch implementation doesn't properly handle symlinks; this must be fixed to ensure file change events trigger correctly when projects contain symlinked shared libraries.

### 3.2 Information volume and computational overhead

The system should be extremely lightweight, as it shares resources with heavy IDEs and local emulators. To accurately track and manage its footprint, the daemon core must accurately monitor its own resource consumption. To do this properly across platforms, the engineering team must replace the unreliable third-party `pidusage` dependency directly with Node's native `process.cpuUsage()` method within `appcd-core`.

To help the core team understand usage volume and identify architectural bottlenecks, the daemon must include robust analytics facilities. The system will deploy an `appcd-telemetry` module specifically designed to safely and asynchronously send analytics events back to the Axway infrastructure. Furthermore, the system must fix the source/user agent support headers in network requests to ensure telemetry data can be properly categorized by the backend.

### 3.3 Developer interface

While the daemon primarily runs in the background, its command-line administrative interface must be intuitive, predictable, and scriptable.

The `appcd status` command is critical for troubleshooting. The team must add support for the `--json` option to the status command so that external tooling can programmatically parse the daemon's health. Crucially, the CLI must display the correct, human-readable status if the daemon is currently not running, rather than throwing a generic socket error.

Configuration must be highly flexible. The CLI interface must add explicit support for `--config` and `--config-file` options, allowing developers to override default behaviors or point to project-specific daemon configurations. Furthermore, the `appcd-config` module must support runtime config updates, allowing the daemon to adjust its behavior without requiring a hard restart.

To assist developers working directly on the daemon itself, the system must automatically start or restart the daemon when watching files in dev mode, preventing the need for manual process termination during the engineering lifecycle.

### 3.4 User characteristics

The intended users of the Appcelerator Daemon are highly technical mobile application developers, enterprise integration specialists, and frontend engineers utilizing the Titanium SDK. They are typically writing client-side code in JavaScript and XML, and rely heavily on the daemon to abstract away the massive complexity of native iOS (Xcode/Objective-C) and Android (Gradle/Java) toolchains. They require a framework that handles complex native SDK integrations seamlessly in the background, never interrupting their primary coding workflows.

### 3.5 Programming language constraints

The primary programming language utilized for the underlying execution engine and local server is JavaScript, specifically executed via Node.js. The performance and security of the daemon rely heavily on how this Node.js runtime is distributed.

To prevent friction during installation, the architecture team must add support for a self-contained, distributable Node executable, ensuring the user does not need to separately manage Node versions just to run the daemon. However, this introduces security constraints on modern operating systems; specifically, within the `appcd-nodejs` module, the framework must ensure it downloads a properly signed node executable on macOS to prevent Apple's Gatekeeper from blocking the daemon.

Dependency management must be strictly curated. The engineering team must execute a sweep across all `appcd-*` modules to completely replace the use of the deprecated `temp` module with the modern `tmp` package. Furthermore, to simplify installation, the team must explicitly remove any dependency on the `optional-dev-dependency` package, and simultaneously improve global package install support across the board.

### 3.6 Process requirements

As an enterprise-grade tooling product, rigorous organizational and testing process requirements must be fulfilled. The repository hygiene and test coverage must be immaculate to prevent regressions in developer environments.

The team must explicitly create a dedicated CI (Continuous Integration) script to orchestrate the automated testing pipelines. Strict mandates require the engineering team to add comprehensive unit tests specifically to the `appcd-plugin`, `appcd-nodejs`, and `appcd-http` modules prior to release.

Finally, the build and distribution pipeline must be entirely automated. Developers must create a standardized `package` task for the top-level gulp file to ensure the daemon can be reliably compiled, zipped, and published to the NPM registry or Axway distribution servers.