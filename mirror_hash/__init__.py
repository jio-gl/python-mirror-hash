"""
Mirror-Hash: An experimental hash function based on Toffoli and Fredkin gates

This module implements the Mirror256 hash function, which is designed 
for optical/quantum computers using Toffoli and Fredkin gates
in a zigzag pattern.
"""

__version__ = '0.2.0'
__author__ = 'José I. O.'
__license__ = 'Apache License 2.0'

from .mirror import Mirror256, new 