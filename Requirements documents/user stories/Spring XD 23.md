As a s-c-d developer, I'd like to investigate how to include/exclude msg bus/binding jars, so I can decide the binding selection and fallback mechanism when there is none setup.
As a s-c-d developer, I'd like to add support for dependency resolution, so when two or more modules use different version of jars (ex: direct binding of two modules that include different versions of spring data), I have the capability to resolve and include the right bits at runtime.
As a s-c-d developer, I'd like to publish the s-c-d image to DockerHub, so I can incrementally push the latest commits to the remote location.
As a s-c-d developer, I'd like to add support for _profiles_ to the core {{Admin}} application, so I can back the stream repository with respective backend strategy. For example: {{local}} profile would use in-memory strategy to store the metadata.
As an s-c-s developer, I'd like to brainstorm and design the foundation to port XD modules as s-c-s modules, so I can use it as the base and start migrating the modules.
As a s-c-d developer, I'd like to add support to expose counter (metrics) endpoints, so I can consume to feed the dashboards to demonstrate {{firehose | counter}} pipe.
As a user I would like to have shell interface to the spring-cloud-data rest API. The scope for this JIRA could be limited to stream commands.
As a s-c-d developer, I'd like to derive a strategy for module metadata via {{@ConfigurationProperties}}, so I can implement {{module info}} command in shell to list all the module properties.
As a Spring XD developer, I'd like to port {{tcp}} module from XD to s-c-s repo, so I can use it as {{source}} module to build streaming pipeline.
As a Spring XD developer, I'd like to move {{twitterstream}} module from XD to s-c-s repo, so I can use it as source modules to build streaming pipeline.
