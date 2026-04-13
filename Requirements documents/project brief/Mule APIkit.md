# Mule APIkit

Mule APIkit is a tool for building Mule REST or SOAP APIs.

1. The developer provides a RAML (RESTful API Modeling Language) specification file to the system via a command-line interface. No graphical user interface (GUI) or IDE integration is required for this version.
2. The system parses the provided RAML file to extract all defined HTTP resources, methods (GET, POST, etc.), and required parameters. Assume the RAML file will not exceed 500 lines. Support for complex file inclusions (e.g., `!include` directives) is out of scope.
3. Based on the parsed RAML, the system automatically generates a single XML configuration file. This XML file must contain an HTTP listener and stubbed routing flows for every endpoint defined in the specification. The generated XML must be properly indented.
4. At runtime, the system acts as an HTTP interceptor. It evaluates incoming web requests against the loaded RAML contract. 
5. The system must enforce strict HTTP compliance: returning HTTP 400 for missing required parameters and HTTP 405 for undefined methods. Valid requests are routed to their corresponding XML flow stubs. No complex payload transformation (e.g., JSON to XML) is required in this initial version.
