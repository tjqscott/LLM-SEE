# Lsstcorp Data management

Lsstcorp Data Management is responsible for creating the software, services and systems which will be used to produce Rubin Observatory?s data products.

1. The data processing administrator manages the LSST Data Management system using command-line Python scripts and an orchestration engine. The system does not interface with the telescope hardware; it strictly operates on raw FITS image files already ingested into a staging directory.
2. The administrator triggers a "Level 1" pipeline run by executing a Python script. The system distributes the image processing tasks across a local compute cluster. Assume the cluster consists of exactly 1,000 static processing nodes. Dynamic auto-scaling of the cluster based on workload is out of scope.
3. The processing nodes execute algorithmic image subtraction (comparing new images against historical templates) to detect transient objects. The output metrics and object coordinates are serialized and loaded into the Qserv distributed database.
4. An astronomer submits an SQL-like query via a dedicated Science User Interface (SUI) API to retrieve object metrics. 
5. The system translates the query, routes it to the appropriate Qserv shards, aggregates the tabular results, and returns them to the astronomer. Visual rendering of the astronomical images within the API response is out of scope; the system returns numerical and tabular data only.
