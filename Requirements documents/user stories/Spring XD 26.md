As a s-c-d developer, I'd like to experiment how do we resolve and then add module dependent JAR's to Boot loader, so I have an approach to handle external libraries required by OOTB modules.
As a s-c-s developer, I'd like to refactor the current {{ModuleLauncher}} contract with Boot's {{JarLauncher}} API, so we don't have to maintain duplicate functionality.
As a s-c-d developer, I'd like to move the external library to its own project, so we have a clear separation of functionalities in s-c-d repo.
As a Spring XD developer, I'd like to port SFTP module from XD to s-c-s repo, so I can use it as source modules to build streaming pipeline.
As a s-c-d developer, I'd like to create a new project to contain all the rules associated {{@RedisRule}} contract, so it is isolated from core functionalities and reusable by test coverage as needed.    Consider moving this coverage to SI commons or equivalent.
As a s-c-d developer, I'd like to create foundation to support _processor_ as OOTB modules, so I can use the processor modules from {{s-c-s-m}} repo to build streaming pipeline.
As a s-c-s developer, I'd like to enable {{offline}} mode for {{AetherModuleResolver}}, so I can pull the module artifacts from local instead of remote maven repo.
As a s-c-d developer, I'd like to create {{ModuleRegistry}} implementation, so I can use this infrastructure to lookup module coordinates by name.
As a s-c-d developer, I'd like to have {{module info}}, {{module list}}, {{module register}}, and {{module unregister}} commands, so I can interact with {{ModuleRegistry}}.
As a s-c-d developer, I'd like to provide optional key-value pairs as deployment properties, so I could leverage them at the runtime to instruct how the modules will be deployed.   _The scope of this story is to specifically support {{count}} to represent {{N}} instances of modules that share the same environment variables._
