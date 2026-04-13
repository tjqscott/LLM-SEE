As an s-c-d user, I'd like to have documentation on deployment manifest, so I could refer to the relevant bits on {{partitions}}. I'd like to understand how streams withe
As an s-c-d user, I'd like to refer to documentation on direct binding, so I can use it as a reference to deploy a stream that includes directly bound modules.   Example: {code} java -jar spring-cloud-stream-module-launcher/target/spring-cloud-stream-module-launcher-1.0.0.BUILD-SNAPSHOT.jar --modules=org.springframework.cloud.stream.module:time-source:1.0.0.BUILD-SNAPSHOT,org.springframework.cloud.stream.module:filter-processor:1.0.0.BUILD-SNAPSHOT,org.springframework.cloud.stream.module:filter-processor:1.0.0.BUILD-SNAPSHOT --args.0.fixedDelay=7 --args.1.expression='payload.contains(6)' --aggregate=true --spring.cloud.stream.bindings.output=filtered {code}
As an s-c-d user, I'd like to {{tap}} the primary pipeline, so I can fork the same data and do some ad-hoc analysis without impacting the original stream.
As an s-c-d user, I'd like to upload custom modules using shell/rest-api, so I can contribute modules and create streaming/batch pipelines.
As a Spring XD developer, I'd like to move {{jms}} module from XD to s-c-s-m repo, so I can use it as source to build streaming pipeline.
As a Spring XD developer, I'd like to move {{mail}} module from XD to s-c-s-m repo, so I can use it as source to build streaming pipeline.
As a Spring XD developer, I'd like to move {{mongo}} module from XD to s-c-s-m repo, so I can use it as source to build streaming pipeline.
As a Spring XD developer, I'd like to move {{mqtt}} module from XD to s-c-s repo, so I can use it as source to build streaming pipeline.
As a Spring XD developer, I'd like to move {{reactor-ip}} module from XD to s-c-s repo, so I can use it as source to build streaming pipeline.
As a Spring XD developer, I'd like to move {{stdout}} module from XD to s-c-s repo, so I can use it as source to build streaming pipeline.
