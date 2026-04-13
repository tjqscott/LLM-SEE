As a consequence of not fixing XD-1289, we should document keys of the form ${xd.stream.name} that are available to users  ${xd.[stream|job].name} and ${xd.container.???} come to mind, there may be others
As a minimum we need some common polling strategy on the client side to detect status changes of job + streams etc. (E.g. during deployment of streams/jobs)  Ideally, I would like to have this addressed on the server-side as well. It would be nice if we could propagate events between, containers and admin-server that would inform about any changes in the system. We could then use those to notify connected UI clients.
As an user, I'd like to have a native _JDBC_ source module to ingest data directly from various databases.
As an user, I'd like to have the ability to ingest data into _Redis_ sink.
As a user, I'd like to have guidance to create custom modules so that I can align the development practices with recommended approach.   11/20: Update: Scope of this task is to create an example to demonstrate and document the capability.
As a user, I'd like to have the option to write into _Kafka_ sink so that I can publish mass data into Kafka broker.
As a user, I'd like to have the option to configure default access control for endpoints so that I can grant access by _Admin_ or _Viewer_ roles.
As a user, I'd like to have the option of _kerberized_ HDFS sink so that I can leverage Kerberos (open source distributed authentication system) for secured data writes into Hadoop.
As a user, I'd like to have the ability to mass-ingest data from various database systems so that I'm not restricted with the current approach (_jdbchdfs_) that is dependent on JDBC drivers.   *Spike Scope:* * Identify integration options * Collaborate to determine the design * Document outcome (design specs)
As a user, I'd like to have the option of _Cassandra_ sink, so I can leverage the NoSQL database to write high volumes of variable data segments in high velocity.
