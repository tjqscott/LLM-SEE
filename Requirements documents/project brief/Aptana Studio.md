# Aptana Studio

Aptana Studio is an open-source integrated development environment (IDE) for building web applications.

1. The software developer interacts with Aptana Studio via a heavy graphical desktop application built on the Java-based Eclipse Rich Client Platform.
2. The developer authors dynamic backend scripts (specifically Python). As the user types, the IDE communicates with a background Python parser via a local network socket. 
3. The parser analyzes the source code (up to 5,000 lines per file) to generate an Abstract Syntax Tree (AST) and returns real-time Code Completion suggestions and syntax highlighting.
4. The editor must mathematically enforce indentation formatting, specifically substituting tabs for spaces based on user preference, and ensuring auto-indentation triggers reliably after comment blocks. Profiling the memory usage or execution speed of the target Python script is out of scope.
5. The developer triggers a local debug session. The IDE spawns an external Python process and attaches an interactive debugger via local sockets. The debugger must reliably pause execution at pre-set breakpoints, support line-by-line stepping, and automatically break execution when an unhandled exception is thrown. Remote server deployment or remote debugging over SSH is out of scope.
