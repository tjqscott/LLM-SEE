# The Titanium SDK

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 The Titanium SDK and its environment.
* 2.2 Product functions: The Cross-Platform UI Framework.


* 3. Other considerations.


* 3.1 Platform-Specific Implementations (iOS & Android)
* 3.2 Core System APIs, Networking, and Persistence
* 3.3 Third-Party Integrations and Media Capabilities
* 3.4 Build Automation, CLI, and Toolchain
* 3.5 Debugging, Deployment, and Console Observability
* 3.6 Process requirements and OS Compatibility



## 1. Introduction

This document delineates the comprehensive software requirements, architectural specifications, and strict systems-level constraints for the instantiation and continuous refinement of **The Titanium SDK**. Engineered as a high-performance, cross-platform mobile development framework, this SDK empowers developers to write applications in JavaScript while delivering fully native, hardware-accelerated user interfaces on both iOS and Android operating systems.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *The Titanium SDK*, and will be referred to as the SDK, the framework, or "the system" in the rest of this document.

The primary purpose of the Titanium SDK is to serve as the foundational software development kit for the Titanium platform. Historically, "cross-platform" mobile development meant wrapping slow, unoptimized HTML5/CSS inside a hidden browser view (a WebView). Titanium fundamentally shifts this paradigm. It introduces a complex binding layer (the Kroll Bridge) that maps JavaScript execution directly to native OS components (e.g., mapping a JavaScript `TableView` instantiation to a native `UITableView` on iOS or a `ListView` on Android).

The high-level goals of this platform instantiation are:
a. To engineer a highly robust, unified UI abstraction layer that exposes native controls—such as buttons, text areas, switches, and sliders—via a single, consistent JavaScript API namespace (`Titanium.UI`).
b. To establish a mathematically precise, thread-safe asynchronous execution environment, specifically resolving critical race conditions within native XMLHttpRequest (XHR) implementations to ensure data integrity during HTTP transfers.
c. To provide an uncompromising build automation toolchain. The architecture must formally introduce Command Line support in the SDK for Build Automation, replacing fragile GUI-only packaging steps and enabling headless Continuous Integration (CI) workflows.
d. To guarantee deep OS-level API access, implementing a comprehensive Filesystem API, Application Settings managers, and robust SQLite Database abstractions.
e. To deliver advanced native integrations, including Push Notifications, Facebook Connect capabilities, and native iPhone Analytics, ensuring enterprise applications possess full feature parity with applications written in Objective-C or Java.
f. To refine the developer experience and deployment telemetry, guaranteeing that console logging accurately reflects deployment states (e.g., differentiating between "installing on emulator" versus "device") and bridging WebView JavaScript errors out to the native console for visibility.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions clarify the complex systems terminology, build concepts, and mobile architecture required for the SDK's implementation:

* *AAPT* – Android Asset Packaging Tool. A critical part of the Android build chain responsible for compiling resources and generating `R.java`.
* *JNI* – Java Native Interface. The programming framework that enables Java code running in a Java Virtual Machine (JVM) to call and be called by native applications and libraries written in other languages (like C/C++).
* *Kroll Bridge* – The proprietary bridging architecture in Titanium that marshals data across the boundary between the JavaScript execution context (V8/Rhino/JavaScriptCore) and the native host OS (Java/Objective-C).
* *Proxy Object* – A JavaScript object that acts as a handle to a corresponding native UI element or system service.
* *Scons* – A software construction tool (written in Python) historically utilized by Titanium to orchestrate the complex multi-step compilation of Android projects.
* *XHR* – XMLHttpRequest. An API available to web browser scripting languages that Titanium natively polyfills to allow HTTP requests from the JavaScript runtime.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the Kroll bridge mechanics and the extensive `Titanium.UI` proxy abstractions. Section 3 covers critical non-functional considerations, including platform-specific routing (Android intents vs. iOS URL handlers), SQLite database constraints, Python-based CLI build scripting, and interactive debugging mechanics.

---

## 2. Requirements description.

### 2.1 The Titanium SDK and its environment.

The following description outlines the intended relationship between the Titanium SDK, the developer's JavaScript code, the embedded JavaScript engines, and the host mobile operating systems:

* **The Runtime Environment:** When a Titanium application is launched, it boots a native shell application. This shell immediately spins up an embedded JavaScript engine (V8 on modern Android, JavaScriptCore on iOS).
* **The Execution Boundary:** The developer's JavaScript executes on a dedicated background thread. When the JavaScript code requests the creation of a UI element (e.g., `Titanium.UI.createButton()`), the Kroll Bridge intercepts this call. It serializes the properties, crosses the thread boundary via an asynchronous message queue, and instructs the native UI thread to instantiate the physical device component.
* **Bi-directional Communication:** If a user physically taps the native button on the screen, the OS fires a native event. The Titanium runtime catches this native event, translates it into a standard JSON payload, and routes it back across the bridge to trigger the developer's JavaScript event listener.

The primary engineering challenge of the SDK is minimizing the latency of this bridge transition. The time taken to execute a cross-boundary call must be strictly minimized, defined mathematically as $t_{bridge} = t_{serialize} + t_{ipc} + t_{deserialize}$, where $t_{ipc}$ is the inter-process/inter-thread communication overhead.

### 2.2 Product functions: The Cross-Platform UI Framework.

The core visual functionalities of the Titanium framework are categorized within the `Titanium.UI` namespace. The SDK must instantiate and map a massive matrix of components:

**Core UI Proxies and Views**

* **Data Presentation:** The SDK must provide highly performant, scrollable lists. The architecture requires full implementation of `Titanium.UI.createTableView` across both primary platforms, ensuring memory recycling (view reuse) is natively handled by the underlying OS adapters to maintain 60 frames per second (FPS) during scrolling.
* **Input Controls:** Form design dictates the creation of versatile input mechanisms. The SDK must support the instantiation of complex input elements via `Titanium.UI.createTextField`, `Titanium.UI.createTextArea`, and `Titanium.UI.createSwitch`. The Android implementation of the switch component must be specifically optimized to match native visual states. To accommodate diverse data entry, the API must add support for displaying different keyboards (e.g., URL, Email, Numeric) dynamically based on text field properties.
* **Interactive Controls:** To capture user intent, the SDK must map standard buttons and sliders, guaranteeing parity via `Titanium.UI.createButton` and `Titanium.UI.createSlider`. For asynchronous feedback, developers require access to `Titanium.UI.createActivityIndicator` to render native, non-blocking loading spinners.

**Navigation and Window Management**

* **Tabbed Interfaces:** Mobile UX relies heavily on tabbed navigation. The framework must implement `Titanium.UI.createTabbedBar` and `Titanium.UI.createButtonBar` for segmented controls. To optimize application startup times, the architecture team must add an option to preload tabs, forcing the instantiation of background tab contexts before the user taps them, masking rendering latency.
* **Context Isolation:** A critical architectural rule must be enforced regarding Window contexts. The system must resolve the defect where `createWindow` in Android does not allow external access; windows operating in distinct heavy-weight Android Activities must be able to resolve and execute shared JavaScript closures via proxy references.
* **System Dialogs:** The framework must access native OS modal dialogs seamlessly. This requires implementing specific wrappers like `Titanium.UI.createEmailDialog` for launching the native OS mail composer with pre-populated attachments.

---

## 3. Other considerations.

### 3.1 Platform-Specific Implementations (iOS & Android)

While the SDK provides a unified API, the underlying implementations often diverge drastically based on Apple's Cocoa Touch and Google's Android frameworks. The SDK must expose platform-specific namespaces (e.g., `Titanium.UI.iPhone` or `Titanium.UI.Android`) for hardware-exclusive features.

* **iOS Implementations:** The iOS module must support deep integration with the Apple Human Interface Guidelines (HIG). The SDK must expose `Titanium.UI.iPhone.createGroupedView` and `Titanium.UI.iPhone.createGroupedSection` to replicate the standard iOS grouped table styles used in settings menus. The navigation stack must be highly customizable, ensuring developers can add custom nav buttons to iPhone apps flawlessly, and dynamically adjust the NavBar Color specifically on the system-generated "More" tab. Furthermore, deep-linking into the app must be supported by allowing iPhone developers to define custom URL handlers via the `Info.plist` bridge.
* **Android Implementations:** Android's security and URL routing mechanics require specific hardening. The WebKit implementation must be patched because Android incorrectly handles `/` and `app://` URLs in `<img>` elements within HTML overlays, failing to resolve local asset paths correctly. Furthermore, the dialog lifecycle on Android is notoriously fragile; the engineering team must resolve fatal `Force close` errors on Android with simple dialogues, and ensure Dialogs are no longer missing the `removeEventListener` capability to prevent memory leaks across Activity contexts.

### 3.2 Core System APIs, Networking, and Persistence

To function as a true application platform, the SDK must provide JavaScript proxies to the mobile device's underlying kernel and hardware subsystems.

* **Database and SQLite:** Titanium provides a local SQL database API backed by SQLite. A critical logic flaw exists in the proxy layer that must be patched: `Database.ResultSet.isValidRow()` currently returns `true` for `CREATE` statements. Because Data Definition Language (DDL) operations do not yield result rows, this function must explicitly return `false` to prevent JavaScript loops from attempting to parse empty memory blocks.
* **Filesystem and Preferences:** The engineering team is mandated to fully implement the Filesystem API (`Titanium.Filesystem`), providing synchronous and asynchronous methods for creating, reading, and deleting files within the application's sandboxed data directories. Similarly, persistent key-value storage must be implemented via the Application Settings (`Titanium.App.Properties`) module.
* **Network and HTTP:** The `Titanium.Network.HTTPClient` is the lifeline for modern apps. The underlying native threading model must be completely audited. A race condition exists in the native XHR `readyState` transitions, where rapid HTTP responses trigger state changes faster than the bridge can dispatch them to JavaScript, resulting in lost callbacks. This must be resolved using thread-safe event queuing.

### 3.3 Third-Party Integrations and Media Capabilities

Enterprise developers rely on third-party SaaS tools. The SDK must provide first-class native modules for these integrations, rather than relying on slow, web-based fallbacks.

* **Cloud and Social:** The system must incorporate API layers for Facebook Connect Integration, mapping directly to the native Facebook iOS/Android SDKs to support Single Sign-On (SSO) without kicking the user to Safari. Furthermore, the system must abstract device token registration to provide a unified API for Push Notifications (APNS on iOS, C2DM/GCM on Android), alongside native iPhone Analytics Integration.
* **Media:** The audio subsystem must be expanded. The SDK must explicitly support decoding and playing the `aacp` radio stream format, allowing developers to build robust internet radio applications. Additionally, the architecture should be modular enough to accommodate Printing Support for outputting documents directly from the device via AirPrint or Google Cloud Print.

### 3.4 Build Automation, CLI, and Toolchain

The process of translating JavaScript and XML configuration files into a compiled `.apk` or `.ipa` is orchestrated by the Titanium Command Line Interface (CLI) and its underlying Python build scripts.

* **Android Scons Pipeline:** The Android build process requires precise orchestration of the Android SDK. A severe architectural defect exists where the internal Android Scons script generates `R.java` in the wrong folder, effectively destroying the linkage between XML layouts and the Java compiler. The build scripts must also be hardened against pathing issues; it must resolve compilation failures when a space in the app name causes issues in the mobile project directory structure, and properly handle Unicode encoding errors when parsing the central `tiapp.xml` manifest file.
* **Headless Builds:** The introduction of Command Line support in the SDK for Build Automation is a strict requirement for the next release. This CLI must output structured status codes and gracefully handle missing dependencies, replacing vague failures where the "Test & Package screen is blank" within the Titanium Studio GUI.

### 3.5 Debugging, Deployment, and Console Observability

The developer feedback loop must be rapid and highly informative. Deploying to physical devices and emulators requires exact telemetry.

* **Console Accuracy:** The deployment scripts must accurately report targets. The system must fix the discrepancy where the console falsely states "installing on emulator" instead of "device" when a physical handset is attached via USB. Furthermore, the deployment engine must be hardened to prevent false positives; it must resolve unexpected errors when installing to a device where the "install succeeds (app seems fine)" but the IDE reports a failure. Generally, it must be made less difficult to tell when an Android application is successfully installed and ready for testing.
* **Interactive Debugger:** The SDK provides a TCP-based JavaScript debugger. The runtime lifecycle must be deeply integrated with this debugger to prevent lockups. Specifically, on Android, the system must resolve a deadlock where, while the debugger is running, the user cannot back out of the app and go back into it without crashing the application's main thread.
* **Error Bridging:** Hybrid UI components (like `Titanium.UI.WebView`) operate in a secondary execution context. The architecture must establish an error-bridging protocol to show WebView JavaScript errors natively in the console, ensuring developers are not flying blind when local HTML assets fail to execute. Furthermore, deep pathing logic within the iOS build chain must be audited to prevent a bad path crash from occurring silently during iPhone Simulator launches.

### 3.6 Process requirements and OS Compatibility

As an SDK targeting global developers, the toolchain itself must be highly resilient across diverse host operating systems (Windows, macOS, Linux).

* **Windows OS Hardening:** The Python build scripts must be meticulously refactored for Windows file path standards (`\` vs `/`). The team must eliminate the catastrophic `WindowsError: [Error 3] The system cannot find the path specified` which currently halts builds on Microsoft OS environments. Furthermore, backward compatibility for host machines is critical; the release engineering team must resolve the environmental issues preventing Windows XP users from getting a successfully created Android project.
* **Legacy and Niche Platforms:** A bug in `modules/tiui/ui.js` regarding the `console.log` function on line 99 must be immediately patched to restore console output integrity. New user onboarding must be protected; the "Newby - Error when launching android application" must be addressed by validating Android SDK paths during project generation before the project won't launch under Developer 0.4.2. Finally, the architectural planning team must continue to assess the feasibility and required scaffolding for supporting alternative Linux-based mobile OS environments, such as Maemo Support.

Only through rigorous adherence to these thread boundaries, build automation requirements, and strict OS API translations can the Titanium SDK provide a flawless, high-performance foundation for enterprise cross-platform mobile development.