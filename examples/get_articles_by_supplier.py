#!/usr/bin/env python3
"""
Example: Get articles from specific DataSuppliers (parts manufacturers)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_tecdoc_client import TecDocClient


# Top DataSuppliers
SUPPLIERS = [
    (3, "ATE"),
    (2, "BOSCH"),
    (7, "SACHS"),
    (206, "A.B.S."),
    (4, "MANN-FILTER"),
]


def main():
    """Get articles from multiple DataSuppliers."""
    
    # Initialize client
    client = TecDocClient()
    
    print("="*80)
    print("TecDoc API - Articles by DataSupplier")
    print("="*80)
    
    for supplier_id, supplier_name in SUPPLIERS:
        print(f"\n{supplier_name} (DataSupplier ID: {supplier_id})")
        print("-" * 80)
        
        # Get articles
        result = client.get_articles(data_supplier_id=supplier_id, page_size=10)
        
        print(f"Total articles: {result['total']:,}")
        print(f"\nFirst 10 articles:")
        
        for i, article in enumerate(result['articles'], 1):
            print(f"  {i:2}. {article['number']:20} - {article['manufacturer_name']}")
    
    print(f"\n{'='*80}")


if __name__ == "__main__":
    main()
