# The MongoDB Engineering

Evergreen is a distributed continuous integration system built by MongoDB. It dynamically allocates hosts to run tasks in parallel across many machines.

1. The release engineer submits a "patch build" request to MongoDB Evergreen via a command-line script. This request contains a local code diff and a list of target build variants (e.g., Ubuntu, Windows).
2. The central Evergreen scheduling server receives the request, parses the directed acyclic graph (DAG) of task dependencies, and queues the tasks. Assume the server will process a maximum of 500 concurrent tasks.
3. The server dynamically allocates ephemeral build agents by calling the AWS EC2 API to spin up virtual machines matching the build variant requirements. Handling multi-cloud provisioning (e.g., Azure or GCP) is out of scope.
4. The allocated EC2 agents execute the compilation and test scripts, streaming the standard output logs directly back to the central server via an HTTP API. 
5. Once the task completes, the central server terminates the EC2 instance and updates the patch build status on a read-only web dashboard.
