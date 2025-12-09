# TecDoc Reference Data

This directory contains reference data extracted from the TecDoc API.

## Files

### car_manufacturers_433.json

**Complete list of all 433 car manufacturers** supported by TecDoc API (Provider ID 23862).

**Source:** TecDoc API `getManufacturers` function  
**Country:** DE (Germany)  
**Last Updated:** 2025-12-09

**Structure:**
```json
{
  "country": "Deutschland",
  "manufacturers": [
    {
      "id": "5",
      "name": "AUDI"
    },
    ...
  ]
}
```

**Statistics:**
- Total manufacturers: 433
- Includes: Passenger cars, motorcycles, commercial vehicles
- Coverage: All major automotive brands worldwide

**Usage Example:**
```python
import json

with open('reference_data/car_manufacturers_433.json', 'r') as f:
    data = json.load(f)
    manufacturers = data['manufacturers']
    
# Find Audi
audi = next(m for m in manufacturers if m['name'] == 'AUDI')
print(f"Audi ID: {audi['id']}")  # Output: Audi ID: 5
```

## Purpose

This reference data is used to:
1. Map manufacturer names to TecDoc IDs
2. Validate manufacturer input
3. Filter articles by car manufacturer
4. Cross-reference with other automotive databases

## Updates

This data is relatively stable but should be refreshed periodically to include new manufacturers.

To update:
```bash
python3 examples/get_manufacturers.py > reference_data/car_manufacturers_433.json
```


---

### parts_manufacturers_77.json / parts_manufacturers_77.csv

**Complete list of all 77 parts manufacturers (DataSuppliers)** available through TecDoc API (Provider ID 23862).

**Source:** TecDoc API `getArticles` function (scanned all DataSupplier IDs)  
**Country:** DE (Germany)  
**Last Updated:** 2025-12-09

**Structure (JSON):**
```json
{
  "total_suppliers": 77,
  "total_articles": 5234567,
  "suppliers": [
    {
      "id": 3,
      "name": "ATE",
      "articles": 14158
    },
    ...
  ]
}
```

**Structure (CSV):**
```csv
DataSupplier ID,Name,Articles
3,ATE,14158
2,BOSCH,1067423
...
```

**Statistics:**
- Total DataSuppliers: 77
- Total Articles: Over 5 million
- Top Supplier: A.B.S. (2,011,654 articles)

**Top 10 Parts Manufacturers:**
1. A.B.S. (ID: 206) - 2,011,654 articles
2. BOSCH (ID: 2) - 1,067,423 articles
3. SACHS (ID: 7) - 526,098 articles
4. SWAG (ID: 8) - 278,537 articles
5. CONTITECH (ID: 32) - 197,577 articles
6. LEMFÖRDER (ID: 12) - 177,379 articles
7. MEYLE (ID: 14) - 100,570 articles
8. CORTECO (ID: 30) - 97,319 articles
9. FEBI BILSTEIN (ID: 29) - 92,820 articles
10. ELRING (ID: 10) - 20,606 articles

**Usage Example:**
```python
import json

with open('reference_data/parts_manufacturers_77.json', 'r') as f:
    data = json.load(f)
    suppliers = data['suppliers']
    
# Find ATE
ate = next(s for s in suppliers if s['name'] == 'ATE')
print(f"ATE ID: {ate['id']}")  # Output: ATE ID: 3
print(f"ATE Articles: {ate['articles']:,}")  # Output: ATE Articles: 14,158
```

**API Usage:**
```python
from core_tecdoc_client import TecDocClient

client = TecDocClient()

# Get all ATE articles
ate_articles = client.get_articles(data_supplier_id=3, page_size=100)
print(f"Total ATE articles: {ate_articles['total']:,}")
```

## Purpose

This reference data is used to:
1. Map parts manufacturer names to DataSupplier IDs
2. Filter articles by specific parts manufacturer
3. Validate DataSupplier input
4. Display available parts manufacturers to users
5. Calculate inventory coverage

## Notes

- DataSupplier IDs are TecDoc-specific identifiers
- Not all manufacturers have the same article coverage
- Article counts may vary by country and provider access level
- Some manufacturers (e.g., BorgWarner) have multiple IDs for different divisions
