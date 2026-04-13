# Apache MXNet

## Software Requirements Initial Report

## Table of Contents

* 1. Introduction


* 1.1 The Project at a Glance
* 1.2 Definitions, acronyms, and abbreviations.
* 1.3 Overview.


* 2. Requirements description.


* 2.1 Apache MXNet and its environment.
* 2.2 Product functions.


* 3. Other considerations.


* 3.1 Reliability of the framework
* 3.2 Information volume and computational overhead
* 3.3 Developer interface
* 3.4 User characteristics
* 3.5 Programming language constraints
* 3.6 Process requirements



## 1. Introduction

This document describes the comprehensive software requirements, architectural specifications, and strategic performance targets for a highly scalable, fault-tolerant system designed to accelerate machine learning research and production deployments. This system is engineered to provide both imperative and symbolic programming interfaces, allowing researchers to build dynamic computational graphs while maintaining the execution speed of highly optimized C++ backends.

### 1.1 The Project at a Glance

The software to be produced will be officially named *Apache MXNet*, and will be referred to as MXNet in the rest of this document. It is defined as an open-source deep learning software framework, used to train, and deploy deep neural networks.

The primary purpose of Apache MXNet is to act as a foundational execution engine for large-scale artificial intelligence workloads. The machine learning community and enterprise organizations currently utilize disparate tools for model training and model inference. Furthermore, existing frameworks often force developers to choose between the flexibility of dynamic graphs and the raw performance of static execution paradigms. MXNet aims to phase out these compromises by providing a unified, hybrid frontend—most notably through its Gluon interface—backed by a heavily optimized, asynchronous C++ engine.

The high-level goals of the new framework iteration are:
a. To drastically improve overall execution speeds by undertaking a massive Cython refactoring initiative across the entire Python frontend.
b. To ensure seamless interoperability with the broader artificial intelligence ecosystem by implementing an Onnx Module to import onnx models into mxnet, as well as establishing MXNet Keras 2.0 Support.
c. To provide a standardized, programmatic interface for high-performance distributed computing by establishing support for distributed training based on NCCL Kvstore.
d. To expand the framework's accessibility to enterprise environments by introducing new MXNet Scala Inference APIs and comprehensive Scala integration.
e. To rigorously protect the stability of the master branch by undertaking an EPIC to create an independent Jenkins Server for MXNet CI (Continuous Integration), allowing for extensive automated testing across heterogeneous hardware architectures.
f. To optimize the memory lifecycle and execution speed of dynamic neural networks by resolving the many-variable create and destroy bottleneck specifically found in gluon dynamic graph execution.

### 1.2 Definitions, acronyms, and abbreviations.

The following alphabetically sorted definitions may help to better understand this document and the complex technical specifications required for the deep learning framework's implementation:

* *Cython* – A programming language that acts as a superset of Python, allowing developers to compile Python code directly to C/C++. The framework mandates extensive Cython Refactoring to bypass the Python Global Interpreter Lock and reduce invocation overhead.
* *Gluon* – An imperative, dynamic neural network interface for MXNet. The framework requires dedicated Gluon Performance optimizations, specifically targeting how the gluon data iterator is constructed.
* *MKL/MKL-DNN* – Math Kernel Library. A highly optimized library of mathematical routines provided by Intel. MXNet will refactor Random and ParallelRandom resources to use MKL specifically for MKL builds.
* *NCCL* – NVIDIA Collective Communications Library. A library providing highly optimized inter-GPU communication. MXNet relies on this for distributed training based on NCCL Kvstore architectures.
* *ONNX* – Open Neural Network Exchange. An open format built to represent machine learning models, which MXNet must support importing.
* *ObjectPool* – A software creational design pattern that uses a set of initialized objects kept ready to use, rather than allocating and destroying them on demand. MXNet will convert created profiling objects to use ObjectPool to reduce memory churn.
* *RecordIO* – A highly efficient binary data format used for sequential data reading. The system must add label augmentation support within the `image recordio2` implementation.

### 1.3 Overview.

The rest of this document contains the required detailed specification for the software. Section 2 presents the core functional requirements of the system, detailing the mathematical operators, the compilation environments, and the deep neural network execution engines. Section 3 mentions other necessary considerations, including performance constraints, developer interfaces, strict process requirements, and continuous integration methodologies.

## 2. Requirements description.

The description of the intended product is detailed in the extensive following subsections, outlining exactly how the core engine, the front-end APIs, and the mathematical operators must behave during both training and inference.

### 2.1 Apache MXNet and its environment.

The following description outlines the intended relationship between MXNet, the physical hardware it runs upon, and its surrounding compilation and execution environment:

* Deep learning models and training scripts flow from user-defined Python or Scala interfaces down to the core C++ execution engine.
* To ensure repository cleanliness and proper dependency isolation, the development team must move submodules to the `3rdparty` folder within the source tree.
* Developer contributions and compilation workflows flow through automated deployment systems. To guarantee hardware compatibility at the edge, the system must actively build Nvidia Jetson and Raspberry Pi as part of CI.
* Furthermore, to support enterprise server environments, the testing infrastructure must also build and test CentOS 7 as part of CI.

The main inputs to MXNet come from developers defining neural network architectures and passing massive multi-dimensional arrays (tensors) through them. It is the job of the system's execution engine to continuously analyze and process these computational graphs, dispatch operations to the appropriate CPU or GPU hardware, and deliver the computed gradients back to the user's optimizer.

### 2.2 Product functions.

The main functional requirements of the system are categorized by their specific architectural domain within the deep learning framework:

**Cython Refactoring and Invocation Performance**
a. The MXNet framework shall completely overhaul its Python bridging layer to reduce interpretative overhead. To address general performance, the engineering team must execute a broad NDArray cython refactoring initiative.
b. The system must eliminate the latency associated with dynamic graph construction. Specifically, developers must refactor the imperative invoke mechanism directly to cython.
c. Data loading pipelines must not bottleneck GPU execution. Therefore, it is required to refactor the gluon data iterator to cython to ensure data is fed to the hardware accelerators efficiently.
d. The framework must heavily optimize its distributed optimization logic by refactoring kvstore-invoked python optimizer code directly to C++ and cython.
e. Memory lifecycle management in the Python frontend must be profiled and corrected. The architecture team must investigate why the `__del__` method takes a long time to execute during object garbage collection.

**Mathematical Operators and Engine Functionality**
f. The MXNet framework shall provide a mathematically rigorous and expansive set of tensor operations. The core engine must be updated to add support for symbolic gradients in the engine, allowing for automatic differentiation across complex computational graphs.
g. The framework must natively support advanced statistical distributions, specifically requiring mathematical function unary ops related to the CDF (Cumulative Distribution Function) of a normal distribution.
h. To support advanced object detection algorithms like Faster R-CNN, the system must add a multi proposal operator (cpu version) and subsequently fix the existing bug in the proposal op (gpu version).
i. The framework must evaluate TensorFlow compatibility patterns, initiating a spike to investigate a `tf.assign` equivalent or alternative for stateful variable mutations.
j. The core arrays must be tightly integrated with hardware accelerators. The team must update ndarray binary ops to use the kernel launch interface for streamlined GPU execution.
k. For dynamic sequence modeling in Natural Language Processing, the system must natively support variable sequence length within the `gluon.RecurrentCell` module.

**Interoperability and API Expansions**
l. The MXNet framework must ensure it does not operate in a silo. The team must build an Onnx Module to import onnx models into mxnet, allowing researchers to train models in PyTorch or CNTK and deploy them using MXNet.
m. The system must cater to high-level framework users by providing explicit MXNet Keras 2.0 Support.
n. To support enterprise deployments running on the Java Virtual Machine (JVM), the framework must introduce robust Scala Inference APIs alongside a dedicated Predictor API.
o. The C-level prediction interface must be expanded; developers are required to add a reshape predicator function to `c_predict_api` to handle dynamic batch sizing during inference.

## 3. Other considerations.

This section provides necessary, non-functional information on what is expected from the system and on characteristics of its environment, including performance metrics, strict reliability mandates, and developer experience requirements.

### 3.1 Reliability of the framework

Reliability of the C++ core engine and the resulting execution environment has a critical priority. The system must guarantee mathematical accuracy and operational stability, which means eliminating fatal crashes during tensor operations. A critical defect must be remediated immediately: the framework currently exhibits a state where `mxnet mkl-dnn` crashes for Max pooling with the convention "full"; this must be patched to prevent deployment panics.

When utilizing diagnostic tools, the system must remain stable. Developers must fix the profiler to allow multiple start/stop commands in the same process without causing segmentation faults or data corruption.

Thread management is paramount in a highly concurrent execution engine. A massive architectural initiative is required for making MXNet thread safe across all of its core dependency injection points and variable mutation interfaces. Furthermore, an architectural spike must be conducted to thoroughly investigate current limitations regarding concurrency and memory management.

### 3.2 Information volume and computational overhead

The system should be able to manage massive terabyte-scale datasets and models with billions of parameters efficiently. To identify deep learning bottlenecks, the system requires extensive profiling tools. The engineering team must prioritize profiling gluon Multi-GPU performance bottlenecks to ensure linear scaling across multiple hardware accelerators.

Furthermore, the system must implement tools for profiling the server process in distributed training environments, specifically when nodes are communicating over the network.

To handle the immense volume of diagnostic data generated during these profiling sessions, the framework must convert created profiling objects to use an `ObjectPool` to prevent memory fragmentation and garbage collection pauses. Additionally, the profiler output must be human-readable, requiring developers to add attributes to the profiling summary data and operator names. Finally, to improve runtime speed and lower memory footprints during forward passes, the framework must implement advanced strategies to cache variables effectively.

### 3.3 Developer interface

The community expressed repeatedly that the developer interface, onboarding experience, and documentation of the system should be a major priority. The project must explicitly document semantics and provide comprehensive tutorials. Specifically, the documentation team must produce a high-quality tutorial for distributed training to guide users in setting up cluster environments.

The compilation and installation experience must be frictionless across different operating systems. The build team must add a basic cython build directly to the `cmake` build system. Furthermore, the system must support Cython build and deployment mechanisms specifically designed for Makefile and/or pip install (utilizing `setup.py` or some other standardized means).

The educational onboarding process must cover all supported languages. Because MXNet relies heavily on enterprise Java ecosystem developers, an update on setting up Scala with MXNet and the IntelliJ IDE is strictly required.

Documentation gaps must be closed prior to the next release cycle. Currently, build instructions for the C++ package are missing; these must be written and integrated into the main repository. The framework must also improve documentation of environment variables, as users frequently misconfigure their hardware bindings due to poor explanations. Finally, the team must provide clear documentation specifically for the `build_version_doc` scripts folder.

### 3.4 User characteristics

The intended users of Apache MXNet are highly technical deep learning researchers, data scientists, and machine learning infrastructure engineers. They are typically writing code in Python, C++, or Scala, which is why providing bug-free bindings across these languages is critical for the framework's adoption. They require a framework that handles complex native hardware integrations (like CUDA and cuDNN) seamlessly behind a friendly, highly expressive dynamic abstraction layer like Gluon.

### 3.5 Programming language constraints

The primary programming languages utilized for the underlying execution engine are C++ and CUDA. However, the performance of the Python frontend is currently unacceptable. To solve this, the framework is enforcing strict programming constraints that heavily rely on Cython to bridge Python to C++ efficiently.

The build tools surrounding the C++ core have specific CMake constraints. The build system must remove the explicitly set `CMAKE_GENERATOR_TOOLSET` directive, as it forces specific compiler versions that break cross-platform compatibility. Furthermore, to speed up local development iteration times, the CMake configuration must allow developers to make an amalgamation build utilizing multiple concurrent jobs.

### 3.6 Process requirements

As the project matures and maintains its status within the Apache Software Foundation, rigorous process requirements must be fulfilled. The CI/CD pipeline is currently a major pain point. Beyond simply establishing the independent Jenkins server, the infrastructure team must ensure that all CI pipelines are deterministic. Currently, transient failures waste engineering hours, so it is a strict mandate to make CI failures locally reproducible.

Repository hygiene must be maintained. The release management team is directed to please delete old releases from the mirroring system to save bandwidth and reduce user confusion.

Academic and research citations are vital to the framework's credibility. The project must simplify the import of citation metadata so researchers can easily reference the MXNet project in their published papers. Finally, the infrastructure team must execute a basic email test to ensure automated notification systems for build failures and repository alerts are functioning correctly.

---

Would you like me to adjust any specific sections of this MXNet requirements document, or perhaps draft a sample of the ONNX import module specifications to see how the API interoperability works in practice?