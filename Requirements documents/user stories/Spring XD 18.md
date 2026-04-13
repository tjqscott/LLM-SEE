As a developer, I'd like to update to Spring Hadoop 2.2.0 GA release, so I can leverage the latest improvements.
As a developer, I in the new development of component (source/processor/sink), how to get the module id and container id  Because components need to generate log, log information must include the unique identifier   xd:>runtime modules
As a developer, I want to be able to override Kafka bus defaults for module consumers and producers, so that I can finely tune performance and behaviour.   Such properties should include - autoCommitEnabled,queueSize,maxWait,fetchSize for consumers - batchSize,batchTimeout for producers
As a PM, I'd like to have XD and XD + Ambari RPM scripts into a single public repo, so that users can go to a single location to use the respective build scripts.
As a developer, I'd like to publish performance benchmarks along with the infrastructure specifics, so the users can use it as a reference while setting up Spring XD cluster.
As a developer, I'd like a job module to be bootstrapped when the job is launched and shut down once it is complete instead of the current behavior of bootstrapping the context when the module is deployed regardless of if it's being used so that I can achieve better resource utilization.
As a user I need to know the Spark streaming features like adding tap at the spark module output and the examples need to be updated. The documentation also needs some more information on `Reliable` receiver.
As a developer, I'd like to have a central place to manage external properties for applications across all the environments, so I can provide server and client-side support for externalized configuration for XD-Admin and XD-Container servers.
As a developer, I'd like to migrate the current MASTER branch CI builds to EC2 instances, so I can manage them all in one-place reliably.
As a developer, I'd like to use spring-cloud-config server for spring-bus modules, so I can centrally manage external properties.
