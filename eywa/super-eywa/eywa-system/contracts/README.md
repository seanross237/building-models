# Contracts

This folder is for the stable Eywa contracts that implementation should build against first.

Current contracts:

- `run-packet-contract.md`
- `node-packet-contract.md`
- `node-output-contract.md`
- `node-record-contract.md`

The point of these contracts is to freeze the bones before runtime code spreads into multiple slightly different shapes.

They define:

- what a run starts with
- what a node starts with
- what a node is allowed to emit
- what must be recorded
