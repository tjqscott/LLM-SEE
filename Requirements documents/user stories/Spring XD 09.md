As a developer, I'd like to build batch sample using _Sqoop_ so that we can demonstrate some of the capabilities.  *Use cases to consider:* * JDBC to HDFS * HDFS to JDBC
As a consequence,  * change gradle script regarding generation of documentation * remove pushGeneratedDocs task, etc * remove link rewriting that is no longer needed
As a field engineer, I'd like to have a comparison of Storm examples in Spring XD so that it is easy to relate from implementation standpoint.
As a PM, I'd like to have the Smart Grid demo (from s1-2014) ported into Spring XD samples repo.
As a developer, I'd like to create a example to demonstrate JDBC to HDFS data movement.
As a user, I'd like to clean up message bus resources associated with the stream so that when the stream is destroyed so does the coupled queues/topics.
As a user, I'd like to clean-up stale queues/topics associated with the stream so when the stream gets destroyed I can clean-up resources.
As a user, I'd like to have the option of editing the deployed/undeployed stream so that I don't have to destroy to just change any deployment property.
As a user, I'd like to include the deployment manifest from the file so that I don't have spend time typing as inline properties.
As a field engineer, I'd like to have reference architectures built on Spring XD so that I can use that as reference building POCs. The scope is to get the raw domain specific ideas captured as first step.
