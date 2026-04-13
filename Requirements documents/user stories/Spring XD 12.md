As a developer, I'd like to host/read Python script (file) from HDFS, so I can use the shell processor in XD (on CF) to delegate data science functionality to Py runtime and receive the feedback back in XD.
As a user, I'd like to have the OOTB _gpfdist_ sink module, so I can use this module to do ultra fast data movement from various sources into GPDB/HAWQ.
As a developer, I'd like to setup UI infrastructure, so I can integrate admin_ui and Flo.
As a developer, I'd like to use an efficient approach to read files, so I don't have to read line-by-line and keep it in-memory in order to consume/write the file content.   Would the _tasklet_ approach be better as opposed to transmitting data via message bus (as streams)?
As a developer, I'd like to create a _gpload_ tasklet, so I can ingest data from various sources into GPDB in an efficient manner.
As a user, I logged in with ROLE_CREATE and I get an error while trying job creation from admin_ui. I can create job from the shell successfully. Trying the same workflow with ROLE_ADMIN results with the same error as well. I don't see anything in the admin/container logs about the error itself.
As a developer, I'd like to add support for explicit partition count configuration, so I can use this option to cleverly route the payload to the intended consumer (module).
As a user, I'd like to have an option to have the hdfs sink use Syncable writes to provide better resiliency in the case of sink/container failures. I'm willing to accept the performance penalty if I choose this option.
As a developer, I'd like to certify Spring XD against PHD 3.0, so I can synchronize with the latest ODP based bits.
As a user, I'd like to have the configuration option to use an alternative DLQ, so I can publish the message this time with additional headers, including one that contains the exception (and stack trace).
