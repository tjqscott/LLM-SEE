# The Mongo C++ Driver

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 The Mongo C++ Driver and its environment.
* 2.2 Product functions: BSON, Connections, and Operations.


* 3. Other considerations.


* 3.1 Reliability, Memory Management, and Initialization
* 3.2 Compilation, Linking, and Distribution
* 3.3 Developer Interface and Header Hygiene
* 3.4 User characteristics
* 3.5 Architectural constraints: C++11 and ABI Compatibility
* 3.6 Process requirements and Testing Metrics



## 1. Introduction

This document delineates the comprehensive software requirements, architectural specifications, and rigorous systems-level constraints for the instantiation and major refactoring of the Mongo C++ Driver. Engineered as an idiomatic C++ interface wrapping the high-performance `libmongoc` C driver, this system provides systems programmers, game engine developers, and high-frequency trading platforms with direct, memory-safe, and highly concurrent access to the MongoDB database.

### 1.1 The Project at a Glance

The software to be produced and standardized will be officially named *The Mongo C++ Driver*, and will be referred to as the driver or "the system" in the rest of this document.

The primary purpose of the Mongo C++ Driver is to provide a native, low-latency conduit between C++ applications and MongoDB clusters. Historically, C++ developers had to rely on cumbersome, heavily coupled client libraries that dragged in massive external dependencies and polluted application namespaces. The core architectural directive for this project phase is to completely rewrite/refactor the C++ client to provide a pristine, decoupled, and highly modular systems library.

The high-level goals of this platform instantiation are:
a. To radically reduce the footprint of the integration by engineering a minimal-dependency BSON library, explicitly mandating that the C++ driver should not require any Boost libraries to use, thereby eliminating massive compile-time overhead for downstream consumers.
b. To establish a strict boundary between the database server source code and the client driver source code, ensuring that the `libmongoclient` artifact absolutely does not link internal server files such as `db/commands.cpp`.
c. To provide an uncompromising, memory-safe execution environment by resolving complex memory leaks, null pointer dereferences during cursor iteration, and race conditions stemming from static initialization order.
d. To guarantee cross-platform C++ Application Binary Interface (ABI) compatibility, enforcing strict compilation flags (such as `/MD` on Windows) and ensuring compatibility with the GCC `--as-needed` linker switch on Linux.
e. To deliver idiomatic Resource Acquisition Is Initialization (RAII) connection semantics, standardizing the `MongoClient` and `ScopedDbConnection` classes to handle connection pooling mathematically safely.
f. To strictly enforce header hygiene for downstream consumers, prohibiting toxic practices such as placing `using namespace std` or `#include <windows.h>` in client-facing headers.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions clarify the complex C++ specific systems terminology required for the driver's implementation:

* *ABI* – Application Binary Interface. The low-level interface between two binary program modules; critical for C++ dynamic libraries (`.so` or `.dll`).
* *BSON* – Binary JSON. The binary-encoded serialization of JSON-like documents. The driver must efficiently map C++ types to BSON byte arrays.
* *GridFS* – A specification for storing and retrieving files that exceed the BSON-document size limit of 16 MB. The driver must fully support GridFS operations, including `slaveOk` querying and metadata manipulation.
* *RAII* – Resource Acquisition Is Initialization. A C++ programming idiom where resource lifecycle (allocations, database connections) is bound to object lifetime (scope).
* *SIOF* – Static Initialization Order Fiasco. A subtle aspect of C++ where the initialization order of static objects defined in different translation units is undefined, causing fatal crashes upon startup.
* *Strict Aliasing* – A C/C++ compiler assumption that pointers of different types do not point to the same memory location, allowing aggressive optimization.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the BSON serialization engine, the socket layer, and the MongoDB API surface. Section 3 covers critical non-functional considerations, including deep C++ memory management, dynamic linking mechanics, header scope hygiene, and continuous integration targets.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core C++ objects, the BSON array builders, the socket abstractions, and the connection pools must behave during standard operation and under heavy concurrent load.

### 2.1 The Mongo C++ Driver and its environment.

The following description outlines the intended relationship between the C++ Driver, the host operating system's networking stack, and the target MongoDB clusters:

* The C++ Driver executes directly within the memory space of the user's application. It acts as an object-oriented wrapper over `libmongoc`, managing the translation of `std::string`, `std::vector`, and standard integral types into BSON wire protocol packets.
* Because high-performance C++ applications often utilize specialized networking stacks (like Epoll, Kqueue, or custom kernel bypasses), the architecture must remain completely un-opinionated regarding transport. The system must allow clients to provide their own implementations of the socket API rather than forcing standard POSIX sockets.
* The driver manages asynchronous or synchronous connections to a MongoDB cluster. Network volatility must be handled gracefully. The system must allow for a configurable connect timeout in the C++ driver (which was previously hardcoded at a fixed 5 seconds), and ensure the underlying polling mechanisms accurately respect this configuration without hanging.

The main inputs to the C++ Driver come from application code invoking the API. It is the job of the driver's execution engine to continuously analyze these inputs, construct highly optimized BSON buffers without unnecessary memory allocations, manage the physical TCP connection lifecycle, and deserialize the returned byte streams back into safe C++ iterator paradigms.

### 2.2 Product functions: BSON, Connections, and Operations.

The core computational functionalities of the C++ Driver are categorized as follows:

**BSON Serialization and Data Types**
a. The driver shall provide a highly performant, type-safe BSON construction API. The architecture team must repair the linking mechanisms to ensure that Mongo C++ BSON code compiles and links properly when utilizing the `BSONArrayBuilder`, which is critical for constructing dynamic lists of documents.
b. Data types must map accurately across locales. The string parsing engine must be hardened to fix the problem with `Query & hint (const string &jsonKeyPatt)` operating against compound indexes in European locales where the comma is used as a decimal point, causing JSON parsers to misinterpret floating-point values.
c. Time representation must be exact. The engineering team is mandated to comprehensively improve date/time support in the C++ driver, bridging `std::chrono` and legacy time structs to precise 64-bit UTC BSON DateTime timestamps.

**Connection Management and MongoDB API**
d. The driver shall expose a standard `MongoClient` object as the primary entry point, completely abstracting the complex connection strings parsing mechanics (which must be updated to support the changes introduced between MongoDB v1.6 to v1.8).

e. Write safety must be fully configurable. The driver must support all Write Concern types (e.g., `w:1`, `w:majority`, `j:true`), allowing the C++ application to specify precisely how many replica set members must acknowledge a write before the thread unblocks.
f. Advanced operational helpers must be implemented natively. The driver must provide a first-class `findAndModify` helper, executing atomic check-and-set (CAS) operations natively.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including the treacherous mechanics of C++ memory management, dynamic library linking across operating systems, namespace isolation, and compiler flags.

### 3.1 Reliability, Memory Management, and Initialization

Reliability in a systems language like C++ requires strict adherence to memory ownership and object lifecycles. A library must never leak memory or invoke undefined behavior.

**The Static Initialization Order Fiasco (SIOF)**
A fundamental architectural defect exists regarding global variables. The C++ standard does not guarantee the order in which static objects across different translation units (source files) are initialized. This has led to a catastrophic crash due to the static initialization order fiasco in the BSON implementation.
To guarantee mathematical determinism, the driver must force explicit initialization. The architecture mandates that developers require driver users to execute `runGlobalInitializersOrDie()` at the very beginning of their `main()` function. However, this function must be thoroughly tested, as currently, `runGlobalInitializersOrDie` returns a `BadValue` exception when invoked specifically via the C++ driver context.
Furthermore, the teardown lifecycle must be cleanly defined. It must be absolutely OK to run the destructors for static objects created by the C++ driver upon application exit without triggering segmentation faults.

**RAII and Pointer Safety**
Memory leaks must be completely eradicated. The engineering team must trace and eliminate phantom memory leaks identified under heavy multithreaded loads. During read operations, the cursor implementation must ensure internally iterated cursor pointers are not null before dereferencing, replacing raw pointers with `std::unique_ptr` where appropriate to enforce ownership semantics.

Connection pooling relies on the RAII pattern via the `ScopedDbConnection` object. A critical design decision must be documented and enforced: if a connection is not explicitly returned to the pool via the `done()` method before the object goes out of scope, the destructor must assume the connection is tainted and destroy the physical socket rather than returning it to the pool. This behavior must be explicitly documented alongside timeout settings.

### 3.2 Compilation, Linking, and Distribution

The driver must be distributed as both a static library and a dynamic shared object (DSO). This requires immaculate handling of linker flags and compiler decorations across Windows and POSIX systems.

**Windows Compilation Constraints**
Windows dynamic link libraries (DLLs) require specific calling conventions. All `MONGO_API` exposed functions must be explicitly decorated with `__cdecl` (or `__stdcall` based on configuration) to prevent stack corruption when the caller and callee assume different stack cleanup responsibilities. The build system must provide an SConstruct option to specify the default Windows calling convention explicitly.

Furthermore, the C Runtime (CRT) library linkage must be strictly enforced. The build system must enforce the `/MD` flag (Multithreaded DLL) with the Windows C++ DLL driver. Mixing `/MT` (static CRT) inside the driver with `/MD` in the user's application results in two distinct heap managers operating in the same process; allocating memory in the driver and freeing it in the application will cause an immediate crash.

**Linux/Unix Compilation Constraints**
On Linux, shared library versioning is critical. It is customary to use SONAMEs when creating shared libraries (e.g., `libmongoclient.so.1`) so the dynamic linker (`ld.so`) can resolve ABI-compatible versions at runtime. The build scripts must ensure that utilizing the shared client compiler switch `--as-needed` does not give compiler errors by stripping out seemingly unreferenced but necessary symbols.

Compatibility with the GNU C Library must be maintained. The build pipeline must resolve the architectural defect where the C++ driver can't compile with `glibc 2.16` due to deprecated system calls or modified struct definitions.

**Distribution and Packaging**
The infrastructure team must heavily improve C++ driver distribution. Red Hat/CentOS deployments must be supported by writing scripts to install client include headers and the shared lib in an RPM package accurately. For Debian/Ubuntu, the engineering team must resolve the issue where the `10gen` repo for Ubuntu does not provide the `mongodb-10gen-devel` package containing the necessary headers. Finally, installation targets in Make/SCons must prevent the duplicate installation of C++ driver headers to `/usr/local/include`.

### 3.3 Developer Interface and Header Hygiene

A C++ library is only as good as its header files. If a library's headers pollute the global namespace, conflict with operating system macros, or force unwanted dependencies on the consumer, it becomes unusable in enterprise codebases.

**Namespace and Include Isolation**
It is a strict violation of C++ best practices to import namespaces in a header. Client-facing headers must absolutely not say `using namespace std` in header scope.

Operating system includes must be isolated. Client-facing headers should not include `<windows.h>`, which defines hundreds of invasive macros (like `min` and `max`) that destroy application code. The driver has already suffered from this: the `numeric_limits::max` compilation problem on Windows occurs precisely because the `max` macro overwrites the `std::numeric_limits` function signature.
Furthermore, the driver must decouple internal definitions, ensuring that `initializer.h` is explicitly included in `dbclient.h` where needed, and that the C++ client driver headers have no dependency on precompiled headers (`pch.h`). Internal hashing functions must be scoped correctly, as global `md5_*` definitions currently cause symbol clashes with OpenSSL or other cryptographic libraries in user space.

**Strict Aliasing and Preprocessor Macros**
The compiler optimizes code based on the Strict Aliasing rule, which dictates that pointers of different, incompatible types cannot point to the same memory location. The `MsgData` class currently casts a `char[4]` byte array directly to an `int*` to read a length prefix.
Let the memory address be denoted by $M$. Accessing $M$ as both a `char` array and an `int` violates strict aliasing. The architecture team must rewrite this using `memcpy` or union punning, as the current cast leads to type alias warnings in C++ clients compiling with strict aliasing warnings as errors (`-Werror=strict-aliasing`).

To assist downstream build systems, the C++ Driver must define a version macro for the preprocessor directly in the headers (e.g., `MONGOCXX_VERSION_MAJOR`), allowing application developers to determine the C++ Driver version from examining the headers and utilizing `#if` directives for backward compatibility.

Finally, the driver must respect the application's standard output. The `DBClientReplicaSet` component must be silenced, as it currently pollutes `stdout` with logging information, breaking CLI applications that rely on clean piped outputs. Exceptions should be the primary error mechanism, but for embedded environments, the architecture should investigate optionally using exceptions versus error codes.

### 3.4 User characteristics

The intended users of the Mongo C++ Driver are deeply technical software engineers writing performance-critical backend services, embedded device logic, or custom database drivers. They require absolute control over memory allocation and networking. They expect the library to be "invisible"—adding zero overhead, introducing zero unrequested dependencies, and compiling flawlessly under the strictest compiler warning levels (e.g., `-Wall -Wextra -Wpedantic`).

### 3.5 Architectural constraints: C++11 and ABI Compatibility

The transition from C++98/03 to C++11 represents a massive shift in the language. The driver must navigate this transition safely.

A critical defect exists where compiling the driver with `-std=c++11` results in a segmentation fault. This is often caused by Application Binary Interface (ABI) breakages. For example, C++11 introduced Small String Optimization (SSO) which changed the memory layout of `std::string` (`sizeof(std::string)` changed). If the driver is compiled as a shared library under C++98, but the user's application compiles with `-std=c++11`, passing a `std::string` across the library boundary will result in an immediate segmentation fault as the two sides interpret the memory layout differently. The build system must enforce that the driver and application are compiled against the exact same C++ standard, providing clear options to add custom CXX flags to the client build.

### 3.6 Process requirements and Testing Metrics

As an enterprise-grade systems library, rigorous compilation testing, continuous integration, and documentation processes must be fulfilled.

The build pipeline must be highly comprehensive. The infrastructure team must add an Evergreen builder specifically for MinGW to ensure continuous compatibility for the open-source Windows compiler toolchain. Furthermore, the CI matrix must strictly verify that all build configurations successfully compile `mongo_client_lib.cpp` and produce the `simple_client_demo(.exe)` binary, as currently, no builders test this exact target.

Documentation must mirror the code perfectly. The technical writing team must review and fix the examples, explicitly addressing the fact that the "Online Array example" in the official documentation is currently not working and contains deprecated API calls. Every action—from the removal of the Boost dependency to the isolation of the `__cdecl` decorations—must be immutably verified, ensuring that the Mongo C++ Driver provides a flawless, memory-safe foundation for high-performance applications.