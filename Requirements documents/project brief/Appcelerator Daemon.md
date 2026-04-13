# Appcelerator Daemon

Appcelerator Daemon The Appcelerator Daemon is a server that runs on a developer?s computer and hosts services which power the tooling for Axway products such as Axway Titanium SDK.

1. The local developer tooling (such as text editors and CLI scripts) interacts with the Appcelerator Daemon by sending HTTP POST requests or establishing persistent WebSocket connections to a local Node.js background server.
2. The daemon receives requests and routes them through a Koa middleware dispatcher to a dynamic set of loaded plugins, such as the Titanium build plugin or the Amplify authentication plugin. 
3. The network layer must support multiplexing, allowing the client tooling to execute up to 5 concurrent asynchronous commands (like tailing a log and triggering a build) over a single, shared WebSocket connection.
4. The daemon must autonomously query the host operating system using detection libraries to locate required dependencies like the Java Development Kit (JDK), Xcode, and connected physical USB devices. The daemon must be distributed as a self-contained Node executable; forcing the developer to install a global Node.js environment on their host machine is out of scope.
5. Concurrently, the daemon monitors the developer's local project directory (maximum 10,000 files) using a filesystem watcher. The watcher must accurately trigger events when symlinked files are modified. Monitoring and synchronizing changes across remote or network-mounted drives (like SMB/NFS) is out of scope.
