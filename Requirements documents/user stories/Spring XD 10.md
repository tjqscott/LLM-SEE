As a user, I'd like to have an optional  arbitrary side channels created so that when creating a module channels other than the primary stream channels (input, output) could be added to the bus (i.e. creating a tap channel *within* a flow). The optional side channels can be used to trace/track module progress.
As a developer, I'd like to benchmark Rabbit performance so that I can use the results as reference to setup XD cluster.
As a developer, I'd like to have the high-level description for each of the modules so that I can use the description (presumably what is captured in javadoc for the module definition) to understand the purpose of the module itself.
As a user, I'd like to have the description for each of the modules so that I can use it to understand the module purpose and it's capabilities (presumably what is captured in javadoc for the module definition).
As a developer, I'd like to research and Identify the EC2 infrastructure required  so that I can run performance tests on Kafka.
As a developer, I'd like to identify the Kafka configurations so that I could setup infrastructure to perform performance testing.
As a developer, I'd like to create EC2 AMI with the necessary packages so that I can run the Kafka Perf tests.
As a developer, I'd like to add load generator _source_ module so that I could use it for performance testing use-cases.
As a developer, I'd like to add load receiving _sink_ module so that I can measure received throughput
As a build manager, I'd like to schedule CI builds for windows so that I can verify XD runtime features/functionality.  The scope is to isolate the remaining test failures; perhaps, experiment with new AMI images until we have a solid infrastructure to fix the failing tests.
