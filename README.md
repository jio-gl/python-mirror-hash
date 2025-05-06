# Mirror-Hash

An experimental hashing algorithm for optical/quantum computers based on Toffoli and Fredkin gates.

This repository contains both Python and Rust implementations of the Mirror256 hash function, a reversible (bijective) hash function based on quantum-inspired logic gates.

## Algorithm

Mirror256 processes input data in 32-byte chunks, applying 128 layers of Toffoli and Fredkin gates arranged in a zigzag pattern:

```
Layer structure (zigzag):
1    ### @@@
2    ###
3    ### @@@
4        @@@
5    ### @@@
6    ###
7    ### @@@
8        @@@
```

Each gate's type (Toffoli or Fredkin) and symmetry (regular or mirrored) is determined by the previous hash block (layer encoding). The function XORs with the current layer encoding to avoid 0-to-0 hashes.

## Features

- 256-bit hash output
- Reversible (bijective) for hash outputs
- Standard state initialization using cubic roots of primes
- Support for Unicode characters
- Proper handling of chunked input processing

## Python Implementation

### Installation

```bash
pip install -e .
```

### Usage

```python
from mirror_hash import Mirror256

# Basic usage
h = Mirror256("Hello, world!")
print(h.hexdigest())

# Incremental hashing
h = Mirror256()
h.update("Hello")
h.update(", ")
h.update("world!")
print(h.hexdigest())

# Using the factory function
from mirror_hash import new
h = new("Hello, world!")
print(h.hexdigest())
```

### Running Tests

```bash
python -m unittest discover python_mirror_hash/tests
```

## Rust Implementation

The Rust implementation provides the same functionality with improved performance.

### Performance Benchmarks (MacBook Air M2)

- Empty string: 37.84 µs
- Short string: 602.86 µs
- Medium string: 1.75 ms
- 1KB string: 18.20 ms
- Throughput: ~411 hashes per second for random 32-byte inputs

## Project Status

This is an experimental hash function designed for educational purposes and to explore reversible computing concepts. It is not recommended for cryptographic applications.

## License

Licensed under the Apache License, Version 2.0
