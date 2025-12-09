#!/usr/bin/env python3
"""
Example: Get all car manufacturers from TecDoc API
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_tecdoc_client import TecDocClient


def main():
    """Get and display all car manufacturers."""
    
    # Initialize client
    client = TecDocClient()
    
    print("="*80)
    print("TecDoc API - Car Manufacturers")
    print("="*80)
    
    # Get manufacturers
    manufacturers = client.get_manufacturers()
    
    print(f"\nTotal manufacturers: {len(manufacturers)}\n")
    
    # Display all manufacturers
    for i, mfg in enumerate(manufacturers, 1):
        print(f"  {i:3}. ID: {mfg['id']:5} | {mfg['name']}")
    
    print(f"\n{'='*80}")
    print(f"Total: {len(manufacturers)} manufacturers")
    print("="*80)


if __name__ == "__main__":
    main()
