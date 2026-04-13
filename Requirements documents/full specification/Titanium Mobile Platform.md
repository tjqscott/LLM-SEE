# Titanium Mobile Platform

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Titanium Mobile and its environment.
* 2.2 Product functions: The API Contract and UI Bridging.


* 3. Other considerations.


* 3.1 Network Protocols and HTTPClient Lifecycle
* 3.2 Application Lifecycle, Contexts, and Modularity
* 3.3 Platform-Specific OS Implementations (iOS vs. Android)
* 3.4 Hardware Integration, Media, and Geolocation
* 3.5 Architectural constraints: The Documentation Engine
* 3.6 Process requirements and SDK Distribution



## 1. Introduction

This document delineates the comprehensive software requirements, architectural specifications, and strict API definitions for the ongoing development and stabilization of the **Titanium Mobile Platform**. Engineered as a high-performance, cross-platform mobile development framework, Titanium provides developers with the tools to build completely native mobile applications for iOS and Android using a unified JavaScript API.

### 1.1 The Project at a Glance

The software and API specifications to be formalized will be managed under the *Titanium Mobile Platform*, and will be referred to as Titanium, the platform, or "the system" in the rest of this document.

Titanium Mobile is a mature platform that abandons the sluggish "HTML5-in-a-WebView" paradigm used by hybrid frameworks. Instead, Titanium employs a complex JavaScript-to-Native bridging architecture. Developers write application logic in JavaScript, and the Titanium runtime dynamically translates UI API calls into their exact native equivalents (e.g., `UIButton` on iOS, `android.widget.Button` on Android).

Because this abstraction layer is so vast, the API Documentation (APIDoc) acts as the absolute source of truth for the system's architectural capabilities. A critical goal of this project phase is to rigorously update, clarify, and enforce the API contract to ensure developers understand the strict underlying memory and rendering constraints of the host operating systems.

The high-level goals of this platform instantiation are:
a. To formalize the complex Window and View hierarchical constraints, explicitly clarifying strict platform limitations, such as the mandate that Windows cannot be added to other Views on Android due to Activity lifecycle boundaries.
b. To rigorously document the asynchronous networking capabilities, specifically updating the `HTTPClient` documentation to reflect its Single-Use architecture and exposing its internal `readyState` machine.
c. To establish precise parity between the documentation and the source code across complex UI components like `TableView`, `Toolbar`, and `TabGroup`, ensuring properties like `headerPullView` and `items` are contractually defined.
d. To solidify the Application and Context lifecycle, thoroughly detailing `pause`, `resume`, `startup`, and `shutdown` events that govern memory allocation and backgrounding across OS boundaries.
e. To modernize the internal documentation generation engine itself, enabling it to support alternative JSON formats and parse granular "since" version numbers on individual methods and properties to support SDK deprecation cycles.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions clarify the complex cross-platform terminology required for the SDK's implementation and API documentation:

* *APIDoc* – The internal structured documentation format used by Appcelerator (the creators of Titanium) to generate the public-facing API website and IDE auto-completion hints.
* *Context* – A distinct JavaScript execution environment within Titanium. Variables and objects created in one context cannot be directly accessed in another without specific bridging techniques.
* *Kroll Bridge* – The proprietary C++/JNI/Objective-C architecture that marshals data back and forth between the V8/JavaScriptCore engine and the native UI threads.
* *View* – The fundamental building block of the Titanium UI (`Ti.UI.View`). It maps directly to `UIView` (iOS) and `android.view.View` (Android).
* *Window* – A top-level container (`Ti.UI.Window`) that maps to a heavy-weight OS construct. On iOS, it usually corresponds to a `UIWindow` or a full `UIViewController`. On Android, it maps strictly to an `Activity`.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the API constraints. Section 2 presents the core functional requirements of the UI components, detailing the `TableView` mechanics, layout properties, and Window hierarchies. Section 3 covers critical non-functional and deep system considerations, including HTTPClient state management, geolocation adapters, hardware camera access, and the internal APIDoc generator architecture.

---

## 2. Requirements description.

### 2.1 Titanium Mobile and its environment.

The Titanium API operates as a facade over vastly different operating systems. When a developer writes code targeting the `Ti.*` namespace, the SDK must seamlessly route that command to the appropriate hardware subsystem.

The environment is highly concurrent. JavaScript executes on a dedicated background thread (the Kroll thread) to prevent blocking the native UI thread. Because of this boundary, API calls that query native UI state or request hardware access must cross an asynchronous bridge. The API documentation must explicitly reflect this reality, warning developers about race conditions, context isolation, and memory management constraints.

### 2.2 Product functions: The API Contract and UI Bridging.

The core visual functionalities of the Titanium framework are categorized within the `Titanium.UI` namespace. The APIDoc must accurately reflect the strict programmatic constraints of these components:

**Window and View Hierarchy**

* **Container Limitations:** The distinction between a "View" (a lightweight UI component) and a "Window" (a heavyweight screen container) is absolute. The architecture team must add a critical note to the APIDoc establishing that adding Windows to Windows is not allowed. Furthermore, because Android Windows are backed by `Activity` instances (which possess their own distinct memory context and lifecycle), the docs must clarify that Windows can't be added to other Views on Android, preventing developers from attempting impossible nested application structures.
* **Layout and Styling:** The positioning engine must be thoroughly defined. The `layout` property for Views and Windows (which accepts `vertical`, `horizontal`, or `composite`) must be documented, and the APIDoc must explicitly "Add Layout to View" to the official property matrix. Foundational styling commands, such as `Titanium.UI.backgroundColor` and `setBackgroundImage()`, must be fully documented with supported formats.
* **Animation Boundaries:** Core graphics transformations must reflect their mathematical limits. The APIDoc must clarify the `animation` API, specifically noting that developers can't rotate 360 degrees in a single animation matrix transformation due to quaternion calculation clamping, requiring two 180-degree rotations instead.

**Complex UI Components: TableViews and Tabs**

* **TableView Mechanics:** The `TableView` is the most memory-intensive UI component. The documentation must encompass all its native capabilities. The `TableView` docs are currently missing the `headerPullView` (which implements the standard "pull-to-refresh" paradigm) and `setContentInsets` (which adjusts scroll boundaries).

Furthermore, strict platform style constraints must be noted: the APIDoc must clarify that no `tableView` font properties are supported at the root level, and `tableViewRow` `font-*` properties are heavily restricted. Finally, the `TableViewRow.editable` property, enabling native swipe-to-delete functionality, must be fully documented.

* **TabGroups:** Tabbed navigation is handled by `Ti.UI.TabGroup`. The documentation must remove Tab click events that are not actually supported by the native SDKs to prevent developer frustration. Platform disparities must be explicit: the APIDoc must add a note to `removeTab()` that it is strictly iOS only (due to Android `TabHost` restrictions), while clarifying that `Ti.UI.TabGroup.removeTab` does indeed take an argument (the tab object).
* **Toolbars:** A `Toolbar` is useless without its buttons. The APIDoc must fix the critical omission where Toolbar documentation is missing the `items` property, which is the array mechanism used to actually populate the Toolbar with proxy objects.

---

## 3. Other considerations.

### 3.1 Network Protocols and HTTPClient Lifecycle

The `Titanium.Network.HTTPClient` acts as the cross-platform Polyfill for the standard web `XMLHttpRequest` (XHR) API, mapping to `NSURLConnection` on iOS and `HttpURLConnection` on Android.

* **Lifecycle and State Management:** Developers frequently misunderstand the memory lifecycle of native HTTP bindings. The APIDoc must update `HTTPClient` to explicitly reflect its "Single Use" nature—an instantiated `HTTPClient` object cannot be reused for a second request; it must be garbage collected and recreated. Furthermore, the internal state transitions (`UNSENT`, `OPENED`, `HEADERS_RECEIVED`, `LOADING`, `DONE`) must be exposed by documenting the `Ti.Network.HTTPClient` `readyState` property.
* **Security and Remote Assets:** When interacting with external servers, security protocols must be observed. The `ImageView` component allows for remote image loading by passing a URL to the `image` property. The APIDoc must include a specific Remote `ImageView` Warning for Secure Sites (HTTPS), detailing how self-signed certificates or proxy configurations impact the asynchronous image downloader. General `ImageView` documentation must also be clarified regarding memory caching semantics.

### 3.2 Application Lifecycle, Contexts, and Modularity

The SDK must provide precise definitions for how JavaScript is loaded into memory and how the application responds to OS-level backgrounding events.

* **Lifecycle Events:** Mobile operating systems aggressively manage application memory. The APIDoc must comprehensively document the `pause` and `resume` events, explaining how the Kroll bridge suspends JavaScript execution when the user switches apps. Additionally, the documentation must add missing `Ti.App` `startup` and `shutdown` events so developers can safely save application state before the OS kills the process.
* **Module Inclusion:** Managing scope in a multi-file Titanium app is complex. The documentation for `Titanium.include` is currently misleading and must be rewritten to explain that it evaluates code in the *current* context, whereas CommonJS approaches use a different mechanism. The APIDoc must also fix a severe documentation bug regarding the `require` function, establishing it as the modern, isolated standard for dependency management.
* **Web Bridging:** When utilizing `Ti.UI.WebView` to host HTML, the boundary between the WebView's JavaScript engine and Titanium's JavaScript engine must be defined. The `WebView.evalJS` docs should provide an explicit example of returning a value from the DOM back across the bridge to Titanium.

### 3.3 Platform-Specific OS Implementations (iOS vs. Android)

Because Titanium is not a "write once, run anywhere" framework, but rather "write once, adapt everywhere," the API contract must meticulously highlight where the platforms diverge visually and programmatically.

* **Android Nuances:** The Android filesystem is deeply complex. The APIDoc contains a misspelling that must be corrected: `"isExteralStoragePresent"` is misspelled in the iOS docs, but correctly spelled as `"isExternalStoragePresent"` on Android, which must be unified. To assist with native Android module development, comprehensive documentation must be written for the `timodule.xml` file, which maps Java classes to Titanium proxies. Finally, the `window.activity` property—which exposes the underlying Android `Activity` object for intent routing—must have its documentation bug resolved to provide accurate usage examples.
* **iOS Nuances:** The iOS ecosystem has distinct visual paradigms. The APIDoc must note that the Keyboard toolbar is not implemented on Android and should be explicitly documented as iPhone-only. Visual rendering glitches, such as the note that on iOS, the "Top endcap stretches a button," must be documented as known SDK behaviors regarding 9-slice image scaling. For iPad-specific layouts, the docs for the `Ti.UI.iPad` module are currently cut off and incomplete; at a minimum, the missing font embedding information must be restored.
* **API Cleanup:** Deprecated or non-existent methods must be purged to maintain trust. The APIDoc must remove references to `Titanium.App.iOS.createBackgroundService`, as this method does not exist in the current bridging implementation.

### 3.4 Hardware Integration, Media, and Geolocation

Titanium provides direct proxy access to device hardware, bridging JavaScript to native OS sensors.

* **Hardware Adapters:** The `Titanium.Media.showCamera` documentation is currently hard to read and interpret. It must be heavily refactored to clearly explain the asynchronous success/error callbacks, `mediaTypes`, and `saveToPhotoGallery` configurations. Similarly, the gesture recognition subsystem (`Titanium.Gesture`) needs immediate updating to clarify how shake events and orientation changes are bubbled up to the JS runtime.
* **Maps and Geolocation:** The mapping subsystem (`Ti.Map`) must be precise. A major oversight must be fixed: the documentation for `Titanium.Map.createView()` is entirely missing and must be added, alongside fixing a broken link in the `Ti.Map.MapView` doc. For Geolocation, the APIDoc must comprehensively document the `reverseGeocoder` API, explaining its reliance on native Apple/Google network services.
* **System Utilities:** The framework must document fundamental utilities. `Ti.Platform.openURL('tel:XXXXXXXXXX')` must be documented to show how the SDK hands off specific URI schemes to the host OS dialer. Cryptographic helpers, specifically `Ti.Utils.sha1`, must be added to the documentation. Additionally, the `JSON` Module (which wraps native JSON parsing) and `Titanium.Contacts.Person.address` must be thoroughly documented to ensure developers can parse address books accurately.

### 3.5 Architectural constraints: The Documentation Engine

To support this massive documentation overhaul, the internal engine used to parse the APIDoc comments and generate the HTML/JSON output must itself be upgraded.

The toolchain must be augmented to support an alternative JSON format output, allowing third-party IDEs (like Appcelerator Studio or Sublime Text plugins) to consume the API definitions for intelligent auto-completion.
Crucially, the API generation schema currently doesn't allow for setting a "since" version number on individual methods and properties. This architectural defect in the documentation generator must be resolved immediately. A mature platform *must* track exactly which SDK version introduced a property (e.g., `@since 1.7.0`) to allow developers to write backward-compatible code.

### 3.6 Process requirements and SDK Distribution

As an enterprise-grade SDK, rigorous organizational documentation and API consistency processes must be fulfilled. The product's adoption relies entirely on the accuracy of its API contract.

The technical writing team and engineering leads must execute a comprehensive sweep of the entire documentation repository:

* The `applicationSupportDirectory` property must be added back to the filesystem docs.
* Method signatures must be clarified, specifically noting that some `Titanium.Filesystem.File` "methods" are actually properties and must be accessed without parentheses.
* Tab documentation bugs must be systematically identified and resolved.
* The documentation for `AlertDialog` must be audited to ensure it is perfectly consistent with the underlying C++/JNI code.
* Examples must be enriched, specifically adding examples for dictionary objects so developers understand how to pass complex configuration hashes into `create*` methods.
* Finally, all broken links in the notes of the Mobile API docs must be identified and repaired, resolving all overarching API Documentation issues.

Only through rigorous adherence to these UI constraints, platform-specific clarifications, and strict documentation standards can the Titanium SDK successfully provide a flawless, secure, and highly performant foundation for the global mobile development ecosystem.

