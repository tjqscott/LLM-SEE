As a s-c-s user, I'd like to have the modules self-register itself with {{Eureka}} whenever they're installed, so I can also discover the same modules using Spring XD Admin SPI and reuse them to create data pipelines.
As a s-c-s user, I'd like to search the modules by it's name aside from the default {{spring.application.name}} offered by boot, so I can also fetch modules by it's name.
As a s-c-s user, I'd like to store module metadata in {{Eureka}}, so I can use the repository to determine the current state.
As a s-c-s user, I'd like to have my modules add/update it's current state to Eureka, so I can use the repository to discover the current sate of the module as needed.
As a Spring XD developer, I'd like to refactor current controller with SPI calls, so I can invoke the respective Admin SPI implementation based on the deployment.   *Controllers to Refactor* * ContainersController * StreamsController * ModulesController * JobsController
As a Spring XD developer, I'd like to self-register {{xd-admin}} server with {{Eureka}}, so I could have admin server exposed as discoverable endpoint.
As a s-c-s developer, I'd like to setup CI builds for s-c-s builds, so I can incrementally build and test code commits automatically.
As a Spring XD developer, I'd like to port {{FTP}} modules from XD to s-c-s repo, so I can use them as {{source}} modules to build streaming pipeline.
As a s-c-s user, I'd like to have the option to direct bind _modules_, so I don't have to use messaging middleware and I can eliminate latency between them. This is important for high throughput and low latency use cases.
As a s-c-d developer, I'd like to establish the foundation to expose REST-APIs to interact with the {{xd-admin}} and likewise perform CRUD operations to maneuver streaming and batch pipelines.
