# Hyperledger Indy SDK

Hyperledger Indy SDK provides a distributed-ledger-based foun- dation for self-sovereign identity. Indy provides a software ecosystem for private, secure, and pow- erful identity, and the Indy SDK enables clients for it. The major artifact of the SDK is a c-callable library; there are also convenience wrappers for various programming languages and Indy CLI tool.

1. The client application developer interacts with the Hyperledger Indy SDK via a native C-callable API. The SDK operates purely as a local library embedded within the developer's application; it does not host a persistent background daemon or web server.
2. The developer uses the SDK to initialize a local, encrypted SQLite wallet database on the client's device. The SDK generates a new private/public key pair and a corresponding Decentralized Identifier (DID). Assume the wallet will store a maximum of 1,000 identity credentials.
3. To authenticate with an external service, the developer instructs the SDK to construct a Zero-Knowledge Proof (ZKP). 
4. The SDK retrieves the necessary encrypted credentials from the local wallet, formats the mathematical proof into a standard JSON payload, and cryptographically signs it using the private key.
5. The SDK transmits this payload securely to a target endpoint using the PairwiseCurveCP encryption protocol. Handling network retries, connection timeouts, or offline queueing is out of scope; the SDK simply attempts the transmission and throws a synchronous error if the network is unreachable.
