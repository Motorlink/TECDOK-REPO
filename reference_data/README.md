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
