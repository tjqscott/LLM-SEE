# Hyperledger Sawtooth

Hyperledger Sawtooth offers a flexible and modular architec- ture separates the core system from the application domain.

1. The blockchain administrator provisions a Hyperledger Sawtooth network by starting a core Validator node via the command line. The Validator node manages network gossip and block consensus (e.g., Proof of Elapsed Time). No graphical administration console is required.
2. The application developer registers a custom "Transaction Processor" with the Validator node via a ZeroMQ (ZMQ) connection. This processor defines a specific "Transaction Family" (a namespace and validation ruleset). Assume a maximum of 5 distinct Transaction Processors will be connected to a single Validator.
3. A Client Application submits a transaction payload (maximum 100KB) to the Validator's REST API. The payload contains a cryptographic signature, the target Transaction Family namespace, and a serialized state-change request. 
4. The Validator verifies the signature and routes the payload to the corresponding Transaction Processor over ZMQ. 
5. The Processor executes the custom business logic, verifies the state constraints, and returns a valid/invalid flag back to the Validator to be included in the next block. Dynamic deployment of smart contracts (e.g., uploading new code to the network at runtime) is out of scope; Transaction Processors must be pre-compiled and manually connected to the Validator.
