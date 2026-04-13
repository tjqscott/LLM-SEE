# Lyrasis Dura Cloud

Lyrasis DuraCloud is a hosted service from LYRASIS that lets you control where and how your content is preserved in the cloud.

1. The archivist interacts with the Lyrasis DuraCloud system via a web-based graphical dashboard to manage institutional digital preservation.
2. The archivist configures connections to external, third-party cloud storage providers (e.g., Amazon S3) by inputting API access keys into the web interface. The system securely encrypts and stores these credentials in its central database.
3. The archivist uploads digital assets (e.g., high-resolution archival TIFFs) via the web dashboard. The system abstracts the underlying cloud provider API and securely transfers the binary payload to the configured storage backend. Assume the system manages a maximum of 10 Terabytes of data per institution. 
4. Public-facing file sharing or direct media streaming from the archive is strictly out of scope; this is a dark storage preservation layer.
5. To ensure data integrity, the system runs an asynchronous background "Compute Service" that periodically calculates MD5 checksums on the stored files and compares them against the original upload hashes. If a discrepancy is found, the system flags the file in the web dashboard. Automatic file repair or fetching from redundant backups is out of scope; the system only reports the integrity failure.
