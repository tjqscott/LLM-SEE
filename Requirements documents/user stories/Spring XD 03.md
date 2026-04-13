As a user, I'd like to have Spring 'Core' upgraded to 4.1.1 (_milestone_ ) so that I can benefit from performance improvements associated with 'compiled' SpEL and other enhancements.
As a user, I'd like to have the flexibility to change the namespace so that I can isolate ZK _metadata_ based on each _tenant_ profile.
As a user, I'd like to type the _username_ and _password_ to gain access to Admin server so that I don't have to add it in some file; hence I don't have to worry about having the password getting logged somewhere.
As a developer, I'd like to have a maintenance branch so that I can commit MINOR release _(ex: 1.0.2)_ code changes instead of committing to MASTER.
As a follow-up action from module registry refactoring we would have to clean-up deprecated functions _(ex: download of module definitions)_ within our codebase.   It may also be necessary to clean-up Shell and Admin-UI modules.
As a user, I'd like to have a config parameter preferably in _servers.yml_ file so that I can enable/disable message rates in the cluster view.
As a user, I'd like to mass ingest data from databases (and others) into HDFS/HAWQ/GPDB so that I don't have to write custom code and as well as be able to ingest in an efficient way.
As a user, I'd like to use Kafka source through simple consumer API (as opposed to high-level) so that I can gain full control to offsets and partition assignment deterministically.  *Spike scope*: - Study simple consumer API functionality - Document findings, approach and next steps
As a user, I'd like to push the custom module (built as uber-jar) via a REST API so that I can install the custom module in cluster.
As a user, I'd like to have a sample app (GitHub project) so that I can use it as a reference while provisioning Spring XD cluster with Kafka.  Consider: * Kafka as message bus * Kafka as source
