# The Mongo C++ driver

A C++ driver for MongoDB based on libmongoc.

1. The C++ systems programmer interacts with the Mongo C++ Driver by linking it as a compiled dynamic shared library within their native application. No graphical administration or external configuration dashboards are required.
2. The programmer explicitly initializes the driver's global state by executing a required setup function (`runGlobalInitializersOrDie`) at the immediate start of their application lifecycle. Failure to call this function will result in a synchronous exception preventing connection initialization.
3. The programmer connects to a MongoDB database cluster by instantiating a connection pool object. The driver manages the physical TCP sockets. Assume the pool is configured to hold a maximum of 10 concurrent connections. 
4. The programmer constructs binary JSON (BSON) payloads using the driver's native, minimal-dependency builder classes. Utilizing external Boost libraries for BSON serialization or networking is strictly out of scope.
5. The application executes a database read operation and receives a memory-safe, iterable cursor object in return. The driver must accurately respect configured connection timeouts; hanging indefinitely on a dropped network packet is prohibited.
