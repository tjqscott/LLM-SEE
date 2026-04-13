# Appcelerator Studio

Appcelerator Studio (TISTUD) Appcelerator Studio is an eclipse based IDE that provides a single, extensible environment to rapidly build, test, package, and publish mobile apps across multiple devices and OSs.

1. The cross-platform developer interacts with Appcelerator Studio via a heavy graphical desktop application built on the Java-based Eclipse Rich Client Platform.
2. The developer authors source code (up to 1,000 files per project), configures project dependencies via visual wizards, and edits the XML project manifest using dedicated graphical editors. 
3. The IDE must bundle a localized Python interpreter internally to ensure background build scripts execute deterministically, without relying on the host machine's global Python path.
4. As the developer types, the IDE's internal parsing engine continuously evaluates the JavaScript files into an Abstract Syntax Tree (AST) to provide real-time Content Assist (CA) and error validation. The syntax parser must strictly enforce and validate against the ECMA-262 5th Edition specification. Support, validation, or transpilation of newer syntax (ES6/ES2015+) is entirely out of scope.
5. To deploy the application, the IDE communicates directly with the local host's native SDKs to compile and push the binary to tethered hardware or local emulators. Cloud-based remote compilation is out of scope; assume all build execution relies strictly on the hardware of the local workstation.
