As a s-c-d developer, I'd like to create {[ModuleRegistry}} stubs, so I can create mock streams by interacting with the registry APIs.
As a s-c-s developer, I'd like to move {{spring-cloud-stream-modules}} from s-c-s to s-c repo, so I can cleanup s-c-s project and at the same time make these modules visible outside of s-c-s.
As a spring-cloud-data developer, I'd like to use an in-memory stream definition repository, so I don't have to spin up a store; obviously, this will not persist between application executions, but it will be useful for a simplified development experience.
As a s-c-d developer, I'd like to invoke REST APIs via shell, so I can validate {{StreamController}} operations.
As a s-c-s developer, I'd like to adapt redis {{counter}} from XD to s-c-s, so I can build streaming pipes using s-c-s modules with simple counters to feed dashboards.
As a s-c-d developer, I'd like to resolve and then add module dependent JAR's to Boot loader, so I have an approach to handle external libraries (ex: database drivers) required by OOTB modules.
As a s-c-s developer, I'd like to _bootify_ {{ModuleLauncher}}, so I can use Spring Boot's support for property, setting, as well as adding options and new functionality in the future, such as CP augmentation.
As a s-c-s developer, I'd like to investigate the right approach to port {{PHD}} as the provider to support {{HDFS}} module from XD, so I can decide better handling of HDFS dependencies, which needs loaded and available in root CP at the runtime.
As a s-c-d user, I'd like to add REST support for stream commands, so I can maneuver streaming pipeline backed by StreamController.
As a s-c-s developer, I'd like to setup CI infrastructure for {{spring-cloud-stream-modules}} (s-c-s-m) repo, so I can build the project continuously on every commits.
