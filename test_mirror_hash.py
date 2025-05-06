#!/usr/bin/env python3
"""
Simple test script to verify that the mirror-hash package works correctly.
"""

from mirror_hash import Mirror256, new

def main():
    # Basic test
    print("Testing Mirror256 hash function:")
    message = "This is the canary."
    h = Mirror256(message)
    print(f"Message: {message}")
    print(f"Hash: {h.hexdigest()}")
    
    # Testing incremental hashing
    h_inc = Mirror256()
    h_inc.update("This ")
    h_inc.update("is the ")
    h_inc.update("canary.")
    print(f"Incremental hash: {h_inc.hexdigest()}")
    print(f"Hashes match: {h.hexdigest() == h_inc.hexdigest()}")
    
    # Testing factory function
    h_factory = new(message)
    print(f"Factory function hash: {h_factory.hexdigest()}")
    print(f"Factory and direct match: {h.hexdigest() == h_factory.hexdigest()}")
    
    # Testing Unicode
    unicode_message = "こんにちは世界"  # Hello World in Japanese
    h_unicode = Mirror256(unicode_message)
    print(f"\nUnicode message: {unicode_message}")
    print(f"Unicode hash: {h_unicode.hexdigest()}")
    
    # Test performance
    import time
    print("\nPerformance test:")
    t_start = time.time()
    count = 0
    while time.time() - t_start < 1:
        test_msg = f"Test message {count}"
        h = Mirror256(test_msg)
        h.hexdigest()
        count += 1
    print(f"Hashes per second: {count}")

if __name__ == "__main__":
    main() 