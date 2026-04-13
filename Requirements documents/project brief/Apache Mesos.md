# Apache Mesos

Apache Mesos is an open-source project to manage computer clusters. It was developed in C++ language at the University of California, Berkeley.

1. The data center administrator and automated distributed frameworks interact with Apache Mesos via a C++ API, a network-based Protocol Buffer messaging layer, and a read-only Web UI.
2. Distributed frameworks (like Hadoop or Spark) submit resource requests to the central Mesos Master node. Concurrently, worker nodes (Slaves) report their available CPU and memory capacity to the Master. 
3. The system must strictly use Protocol Buffers for all inter-node communication; parsing JSON or XML messaging formats over the network is out of scope.
4. The Master's allocation module processes the available capacity and issues execution directives to the Slaves. The Slaves utilize Linux Containers (LXC) to partition the hardware and execute the tasks. Assume a maximum static cluster size of 1,000 Slave nodes for this specification.
5. If a task attempts to exceed its allocated memory limit, the LXC isolation module must aggressively kill the entire container to protect the host node. Graceful memory swapping or dynamic reallocation is out of scope.
6. During execution, Slaves capture stdout and stderr streams and transmit them to the Web UI. The Web UI must dynamically display this historical execution data in sortable tables. Initiating new framework deployments or mutating cluster state directly from the Web UI is out of scope; the GUI is strictly for observability.
