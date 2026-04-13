# Atlassian Clover

Atlassian Clover Clover is a Java code coverage analysis utility bought and further developed by Atlassian.

1. The Java QA automation engineer interacts with Atlassian Clover via command-line build tools (specifically Maven or Ant) and native IDE plugins. No standalone graphical desktop application is required for this utility.
2. During the compilation phase of the build pipeline, the Clover instrumentation engine parses the Java source code (handling codebases up to 500,000 lines) into an Abstract Syntax Tree (AST). 
3. It injects coverage-tracking counters into the bytecode and outputs the instrumented classes. Instrumenting or tracking dynamically generated proxy classes (like Spring CGLIB proxies) at runtime is out of scope.
4. The automated test suite executes the instrumented classes on the JVM. The injected counters record line and branch execution outcomes, saving the binary coverage data to local database files. For multi-module projects, the system utilizes a thread-safe merge task to aggregate these disparate database files into a single unified metric.
5. The reporting engine reads the aggregated database and generates HTML and XML reports. The engine must map the obfuscated/instrumented stack traces back to their original source code line numbers, and output visual density maps (per-package coverage clouds) to highlight untested areas of the repository.
