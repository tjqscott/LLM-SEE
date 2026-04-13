# The Titanium SDK

The Titanium SDK is the software development kit for Titanium platform.

1. The mobile application developer interacts with the Titanium SDK by writing JavaScript source code and executing a local Python-based Command-Line Interface (CLI) build script. No cloud-based remote compilation services are required; all builds occur on the developer's local workstation.
2. The developer defines application user interfaces and business logic within the JavaScript files. At runtime on the mobile device, an embedded JavaScript engine executes this code on a background thread.
3. When the JavaScript code requests the creation of a UI component (e.g., a button or table view), the system's internal C++ bridge intercepts the call, serializes the property data, and instructs the host operating system's main thread to instantiate the physical, native UI element. 
4. Wrapping web-based HTML5 elements inside a hidden browser view (WebView) to fake UI components is strictly out of scope.
5. The developer invokes an asynchronous HTTP request using the framework's networking API. The system translates this into a native OS network call. The bridge must queue asynchronous state transitions in a thread-safe manner to ensure the JavaScript callback executes sequentially without dropping race-condition events.
