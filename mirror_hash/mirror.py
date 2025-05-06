#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mirror256 Hash Function

An experimental hash algorithm for optical/quantum computers based on 
Toffoli and Fredkin gates organized in a zigzag pattern.

Copyright 2024 José I. O.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import struct
import binascii
import random
from typing import List, Optional, Union

def new(m: Optional[str] = None) -> 'Mirror256':
    """Create a new Mirror256 hasher instance."""
    return Mirror256(m)

def cubic_root_array(cr: int) -> List[int]:
    """Convert a cubic root to an array of 8 hex digits."""
    h = format(cr, 'x')
    while len(h) < 10:
        h = '0' + h
    ret = [0] * 8
    h = h[-10:-2]  # Extract the 8 digits
    for i in range(8):
        if i < len(h):
            ret[i] = int(h[i], 16)
    return ret

class Mirror256:
    """
    Mirror256 Hash Function, Provable Reversible (Bijective) for Hashes.
    
    This hash function uses Toffoli and Fredkin gates arranged in a zigzag pattern
    to process input data in 32-byte chunks. The function is designed for 
    optical/quantum computers.
    """

    # Constants for configuration
    DEFAULT_DEPTH = a = 128  # Number of layers
    DEFAULT_SIZE = 256       # Output size in bits
    
    # Gate types
    TOFFOLI = 0
    FREDKIN = 1
    
    # Gate symmetry
    REGULAR = 0
    MIRRORED = 1
    
    # First primes cubic root representation (truncated for brevity)
    # This is used for initializing the standard state
    # fmt: off
    FIRST_PRIMES_CUBIC_ROOT_DEC_REP = [
        0xa54ddd35b5, 0xd48ef058b4, 0x342640f4c9, 0x51cd2de3e9, 0x8503094982, 0x9b9fd7c452, 0xc47a643e0c, 0xa8602fe35a,
        0x20eaf18d67, 0x4d59f727fe, 0x685bd4533f, 0x7534dcd163, 0x8dc0dcbb8b, 0xb01624cb6d, 0xcfeabbf181, 0xda0b94f97e,
        0x8f4d86d1a9, 0x20c96455af, 0x29c172f7dd, 0x43b770ba12, 0x544d18005f, 0x6c34f761a1, 0x8a76ef782f, 0x98f8d17ddc,
        0xa0151027c6, 0xae080d4b7b, 0xb4e03c992b, 0xc251542f88, 0x3dc28be52f, 0xb75c7e128f, 0x241edeb8f4, 0x04317d07b2,
        0x46305e3a3d, 0x4bafebecef, 0x09308a3b6b, 0x6bb275e451, 0x76044f4b33, 0x85311d5237, 0x94051aaeb0, 0x98e38ef4df,
        0xb0b5da348c, 0xb55fd044a0, 0xbe9b372069, 0xc32ceea80e, 0xddf799a193, 0x0eee44484b, 0x17529bf549, 0x1b7b53489d,
        0x23ba4d74a0, 0x2febef5a50, 0x33f0db9016, 0x47b5d89777, 0x5352304156, 0x5ec09f1622, 0x6a02e0a83b, 0x0af9027c88,
        0x78c3f873a6, 0x8009496a17, 0x83a5537ad2, 0x95715f4210, 0xadb0de7719, 0xb47bab87d1, 0xb7db7bc375, 0xbe90221e69,
    ]
    # fmt: on
    
    # Class variable to store hash states
    _last_hashes: List[List[int]] = []
    
    def __init__(self, m: Optional[str] = None, depth: Optional[int] = None, 
                 size: Optional[int] = None, use_standard_state: bool = True):
        """
        Initialize a new Mirror256 hasher.
        
        Args:
            m: Optional initial message to hash
            depth: Number of layers (default: 128)
            size: Output size in bits (default: 256)
            use_standard_state: Whether to use standard state initialization
                               based on cubic roots of primes
        """
        self._buffer = ""
        self._counter = 0
        self.depth = depth or self.DEFAULT_DEPTH
        self.size = size or self.DEFAULT_SIZE
        self._hashed = []
        
        # Initialize the state
        if len(self._last_hashes) < self.depth:
            if use_standard_state:
                self._init_standard_state()
            else:
                self._init_random_state()
        
        # Process initial message if provided
        if m is not None:
            if not isinstance(m, str):
                raise TypeError(f"{self.__class__.__name__}() argument 1 must be string, not {type(m).__name__}")
            self.update(m)
    
    def _init_standard_state(self) -> None:
        """Initialize the state with cubic roots of primes."""
        while len(self._last_hashes) < self.depth:
            i = len(self._last_hashes)
            layer = []
            if i < len(self.FIRST_PRIMES_CUBIC_ROOT_DEC_REP):
                jprimerep = self.FIRST_PRIMES_CUBIC_ROOT_DEC_REP[i]
                layer.extend(cubic_root_array(jprimerep))
                
                # Fill the rest of the layer with non-zero values
                while len(layer) < self.size // 4:
                    layer.append(((i + 1) % 16))
                
                self._last_hashes.append(layer)
            else:
                # Use a deterministic pattern for remaining layers
                layer = [(i + j) % 16 for j in range(self.size // 4)]
                self._last_hashes.append(layer)
    
    def _init_random_state(self) -> None:
        """Initialize the state with random values."""
        random.seed(777)  # Use fixed seed for deterministic results
        while len(self._last_hashes) < self.depth:
            random_hash = [random.randint(0, 15) for _ in range(self.size // 4)]
            self._last_hashes.append(random_hash)
    
    def _unpack(self, m: str) -> List[int]:
        """Unpack a string into an array of nibbles."""
        ret = [0] * 64
        # Convert string to bytes if not already
        if isinstance(m, str):
            m_bytes = m.encode('utf-8')
        else:
            m_bytes = m
            
        # Ensure we have exactly 32 bytes
        m_bytes = m_bytes[:32].ljust(32, b'A')
        
        # Unpack the bytes
        l = struct.unpack('!32B', m_bytes)
        i = 0
        for b in l:
            # high nibble
            ret[i] = (b >> 4) & 0x0F
            i += 1
            # low nibble
            ret[i] = b & 0x0F
            i += 1
        return ret
    
    def _pack(self, hm: List[int]) -> bytes:
        """Pack an array of nibbles into a byte array."""
        hb = [0] * (self.size // 8)
        for i in range(self.size // 8):
            if i * 2 < len(hm):
                b = hm[i * 2] << 4
                if i * 2 + 1 < len(hm):
                    b = b | hm[i * 2 + 1]
                hb[i] = b
        return struct.pack(f'!{self.size // 8}B', *hb)
    
    def digest(self) -> bytes:
        """Return the digest as a byte array."""
        return self._pack(self._hashed)
    
    def hexdigest(self) -> str:
        """Return the digest as a hexadecimal string."""
        return '0x' + binascii.hexlify(self.digest()).decode('ascii')
    
    def update(self, m: str) -> None:
        """
        Update the hash with more data.
        
        Args:
            m: The message to hash
        """
        if not m:
            return
        
        if not isinstance(m, str):
            raise TypeError(f"update() argument 1 must be string, not {type(m).__name__}")
        
        self._buffer += m
        self._counter += len(m)
        
        # Process complete 32-byte chunks
        while len(self._buffer) >= 32:
            chunk = self._buffer[:32]
            hm = self._mirror256_process(chunk)
            self._last_hashes = [hm] + self._last_hashes[:self.depth-1]
            self._buffer = self._buffer[32:]
        
        # Process any remaining data
        if self._buffer or m == '':
            padded = self._buffer + 'A' * (32 - len(self._buffer))
            hm = self._mirror256_process(padded)
            self._hashed = hm
    
    def _mirror256_process(self, m: str) -> List[int]:
        """Process a 32-byte chunk and return the hash."""
        block = self._unpack(m)
        
        # Apply all hash layers
        for layer in range(self.depth):
            block = self._hash_layer_pass(layer, block)
        
        return block
    
    def _hash_layer_pass(self, layer: int, block: List[int]) -> List[int]:
        """
        Apply a single hashing layer.
        
        Layer structure (zigzag):
        1    ### @@@
        2    ###
        3    ### @@@
        4        @@@
        5    ### @@@
        6    ###
        7    ### @@@
        8        @@@
        
        Each gate can be Toffoli or Fredkin, mirrored or not (4 choices).
        """
        layer_hash = self._last_hashes[layer]
        block = block.copy()  # Create a copy to avoid modifying the original
        
        # XOR with layer encoding to avoid 0 to 0 hashes
        for gate_index in range(self.size // 4):
            if gate_index < len(block) and gate_index < len(layer_hash):
                block[gate_index] = block[gate_index] ^ layer_hash[gate_index]
        
        # First sublayer
        for gate_index in range(self.size // 4):
            if gate_index < len(layer_hash):
                gate_type = layer_hash[gate_index] & 0x3
                
                gate_name = gate_type & 1  # Toffoli (0) or Fredkin (1)
                gate_symmetry = gate_type >> 1  # Regular (0) or Mirrored (1)
                
                block = self._apply_gate(gate_index, gate_name, gate_symmetry, block, True, layer)
        
        # Second sublayer
        for gate_index in range(self.size // 4):
            if gate_index < len(layer_hash):
                gate_type = (layer_hash[gate_index] & 0xC) >> 2
                
                gate_name = gate_type & 1  # Toffoli (0) or Fredkin (1)
                gate_symmetry = gate_type >> 1  # Regular (0) or Mirrored (1)
                
                block = self._apply_gate(gate_index, gate_name, gate_symmetry, block, False, layer)
        
        return block
    
    def _get_wire(self, gate_index: int, first_sublayer: bool, offset: int = 0) -> int:
        """Get the wire index for a gate."""
        return (gate_index * 4 + offset + (2 if not first_sublayer else 0)) % self.size
    
    def _get_bit(self, block: List[int], wire: int) -> int:
        """Get the bit value at a specific wire."""
        if wire // 4 < len(block):
            return (block[wire // 4] >> (wire % 4)) & 1
        return 0
    
    def _set_bit(self, block: List[int], wire: int, bit: int) -> List[int]:
        """Set the bit value at a specific wire."""
        if wire // 4 < len(block):
            old_nib = block[wire // 4]
            ret = (old_nib & (15 ^ (1 << (wire % 4)))) | (int(bit) << (wire % 4))
            block[wire // 4] = ret
        return block
    
    def _apply_gate(self, gate_index: int, gate_name: int, gate_symmetry: int, 
                   block: List[int], first_sublayer: bool, layer: int) -> List[int]:
        """
        Apply a gate (Toffoli or Fredkin) to the block.
        
        Args:
            gate_index: Index of the gate
            gate_name: Type of gate (0=Toffoli, 1=Fredkin)
            gate_symmetry: Symmetry of gate (0=Regular, 1=Mirrored)
            block: Current block state
            first_sublayer: Whether this is in the first sublayer
            layer: Current layer number
        
        Returns:
            Updated block after applying the gate
        """
        initial_offset = layer % 2
        wire1 = self._get_wire(gate_index, first_sublayer, offset=initial_offset + 0)
        wire2 = self._get_wire(gate_index, first_sublayer, offset=initial_offset + 1)
        wire3 = self._get_wire(gate_index, first_sublayer, offset=initial_offset + 2)
        
        val1 = self._get_bit(block, wire1)
        val2 = self._get_bit(block, wire2)
        val3 = self._get_bit(block, wire3)
        
        oval1, oval2, oval3 = val1, val2, val3
        
        # Toffoli and Regular
        if gate_name == self.TOFFOLI and gate_symmetry == self.REGULAR and (val1 and val2):
            val3 = val3 ^ (val1 and val2)
        # Toffoli and Mirrored
        elif gate_name == self.TOFFOLI and gate_symmetry == self.MIRRORED and (val2 and val3):
            val1 = val1 ^ (val2 and val3)
        # Fredkin and Regular
        elif gate_name == self.FREDKIN and gate_symmetry == self.REGULAR and val1 and val2 != val3:
            val2, val3 = val3, val2
        # Fredkin and Mirrored
        elif gate_name == self.FREDKIN and gate_symmetry == self.MIRRORED and val3 and val1 != val2:
            val1, val2 = val2, val1
        
        # Update block with new values
        block = block.copy()  # Create a copy to avoid modifying the original
        
        if val1 != oval1:
            block = self._set_bit(block, wire1, val1)
        if val2 != oval2:
            block = self._set_bit(block, wire2, val2)
        if val3 != oval3:
            block = self._set_bit(block, wire3, val3)
        
        return block


def random_alphanumeric_string(length: int) -> str:
    """Generate a random alphanumeric string of the given length."""
    import string
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


if __name__ == "__main__":
    # Simple demonstration of the hash function
    import time
    
    random.seed(777)
    message = 'This is the canary.'
    print(f'Message: {message}')
    
    h = Mirror256(m=message)
    print(f'Hash: {h.hexdigest()}')
    
    # Benchmark
    print("\nBenchmarking...")
    t = time.time()
    count = 0
    
    while time.time() - t < 1:
        rand_str = random_alphanumeric_string(32)
        h = Mirror256(rand_str)
        h.hexdigest()
        count += 1
    
    print(f'{count} hashes per second')
    
    # Example with a specific message
    example_msg = 'This is the canary #42. asdfasdfasdfasdfasdfqwerqwerqwerdfnnjkdfnjldljknsvv'
    h = Mirror256(example_msg)
    print(f'\nExample message: {example_msg}')
    print(f'Example digest: {h.hexdigest()}')
    
    # Example with random string
    rand_msg = random_alphanumeric_string(32)
    h = Mirror256(rand_msg)
    print(f'\nRandom message: {rand_msg}')
    print(f'Random digest: {h.hexdigest()}') 