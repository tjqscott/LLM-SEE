# Command-Line Interface

Appcelerator Command-Line Interface Command-Line Interface is provided by Ap- pcelerator to check and configure environment setup, create, and build applications.

1. The mobile developer interacts with the Appcelerator Command-Line Interface (CLI) strictly through a local terminal (e.g., Bash or Windows Command Prompt) by executing the `appc` Node.js binary. No graphical installer or setup wizard is required.
2. The developer executes commands to scaffold new Titanium and Arrow projects, validate local environment paths, and trigger compilation pipelines. 
3. Scaffolding support is strictly limited to Titanium modules and Arrow applications; generating raw native Swift, Objective-C, or Kotlin scaffolding is out of scope.
4. Upon receiving a build command, the CLI orchestrates the compilation of application assets (up to 500MB) by validating local dependencies and invoking external native build tools like Xcode's xcodebuild or the Android SDK's aapt. 
5. The CLI must maintain completely isolated build state directories, ensuring that concurrent compilation for an iOS simulator and an Android emulator does not result in artifact cross-contamination.
6. The CLI must guarantee offline availability for local development. If the system attempts to verify authentication or synchronize with the Appcelerator Cloud Services (ACS) and encounters a network timeout, the CLI must gracefully handle the 504 error and proceed with local compilation unconditionally.
