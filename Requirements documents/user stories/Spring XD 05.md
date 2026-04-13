As a build manager, I'd like to setup CI infrastructure so that I can run integration tests in Windows OS automatically as we commit-trigger new builds.   *Scope:* * Use the environment where Bamboo is running * Gain access to powershell  * Setup services (redis, rabbit, etc.) * Kick-off CI task
As a QA, I'd like to include acceptance test coverage for _spark-app_ batch job so that I can validate the functionality as part of every CI build.
As a QA, I'd like to include acceptance test coverage for _Kafka_ as a message bus so that I can validate the functionality as part of every CI build.
As a user, I'd like to have concurrency and compression support for Kafka so that I can increase performance throughput and/or increase responsiveness  *Things to consider:* * make global configuration options be defaults and allow per-deployment overrides * add options for  ** concurrency ** compression support
As a user, I'd like to have the option to _ACK_ messages so that I can guarantee that the message/request sent is successful.
As a user, I'd like to have the option to implement _bindRequestor_ and _bindReplier_ so that I can bind a producer that expects async replies and bind a consumer that handles requests from a requestor and asynchronously sends replies respectively.
As a user, I'd like to have the option to setup _batching_ so that I can ingest data in batches as opposed to payload-at-a-time.
As a user, I'd like to have the option to _stop_ an existing Sqoop job so that I can clean-up resources at the time of completion.
As a user, I'd like to access Sqoop logs so that I can troubleshoot or evaluate the errors or current state respectively.   We will have to identify how to capture the Sqoop logs and stream them to our logging mechanism.
As a QA, I'd like to benchmark _Sqoop_ vs. _jdbchdfs_ batch job so that I can compare and contrast performance stats.
