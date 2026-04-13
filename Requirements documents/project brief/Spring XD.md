# Spring XD

Spring XD makes it easy to solve common big data problems such as data ingestion and export, real-time analytics, and batch workflow orchestration

1. The data engineer interacts with the Spring XD central administration node by submitting a text-based Domain Specific Language (DSL) string via a REST API to define a data processing pipeline.
2. The central node parses the DSL string (e.g., `http | filter | hdfs`) and deploys the corresponding ingestion, processing, and export modules across a distributed cluster of worker containers. 
3. The system utilizes a Redis-backed message bus to route data between these modules. Assume a maximum cluster size of 50 worker containers.
4. The deployed ingestion module receives high-velocity incoming data via a non-blocking, Project Reactor-based network receiver. The ingestion layer must process network events asynchronously; utilizing a legacy thread-per-connection blocking I/O model is strictly out of scope.
5. Processed data tuples are routed to an export module and written in batches to a Hadoop Distributed File System (HDFS). 
6. The HDFS export module must natively compress the outbound files using algorithms like Snappy or GZIP prior to writing the blocks to disk.
