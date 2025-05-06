#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for the Mirror256 hash function.
"""

import unittest
from mirror_hash import Mirror256, new

class TestMirror256(unittest.TestCase):
    """Test cases for the Mirror256 hash function."""

    def test_empty_string(self):
        """Test hashing an empty string."""
        h = Mirror256("")
        digest = h.hexdigest()
        self.assertIsNotNone(digest)
        self.assertTrue(digest.startswith("0x"))
        self.assertEqual(len(digest), 66)  # "0x" + 64 hex chars

    def test_basic_string(self):
        """Test hashing a basic string."""
        h = Mirror256("This is the canary.")
        digest = h.hexdigest()
        self.assertIsNotNone(digest)
        self.assertTrue(digest.startswith("0x"))
        self.assertEqual(len(digest), 66)  # "0x" + 64 hex chars

    def test_new_factory(self):
        """Test the new() factory function."""
        h1 = Mirror256("test string")
        h2 = new("test string")
        self.assertEqual(h1.hexdigest(), h2.hexdigest())

    def test_update(self):
        """Test incremental hashing with update()."""
        h1 = Mirror256("Hello, world!")
        
        h2 = Mirror256()
        h2.update("Hello")
        h2.update(", ")
        h2.update("world!")
        
        self.assertEqual(h1.hexdigest(), h2.hexdigest())

    def test_unicode(self):
        """Test hashing Unicode strings."""
        text = "こんにちは世界"  # "Hello World" in Japanese
        h = Mirror256(text)
        digest = h.hexdigest()
        self.assertIsNotNone(digest)
        self.assertTrue(digest.startswith("0x"))
        self.assertEqual(len(digest), 66)  # "0x" + 64 hex chars

    def test_consistency(self):
        """Test that the same input always produces the same hash."""
        input_str = "The quick brown fox jumps over the lazy dog."
        h1 = Mirror256(input_str)
        h2 = Mirror256(input_str)
        self.assertEqual(h1.hexdigest(), h2.hexdigest())

    def test_long_input(self):
        """Test hashing a long input (more than 32 bytes)."""
        long_input = "a" * 100
        h = Mirror256(long_input)
        digest = h.hexdigest()
        self.assertIsNotNone(digest)
        self.assertTrue(digest.startswith("0x"))
        self.assertEqual(len(digest), 66)  # "0x" + 64 hex chars

if __name__ == "__main__":
    unittest.main() 