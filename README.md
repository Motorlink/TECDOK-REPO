# TecDoc API Integration

Complete Python integration for TecAlliance TecDoc Web Service API (Pegasus 3.0).

## Overview

This repository contains a fully functional Python client for the TecDoc API, providing access to automotive parts data for Germany (DE).

## Features

- ✅ **SOAP API Integration** - Full support for TecDoc Pegasus 3.0 SOAP endpoints
- ✅ **77 DataSuppliers** - Access to over 3 million automotive parts
- ✅ **433 Car Manufacturers** - Complete vehicle manufacturer database
- ✅ **Modular Architecture** - Clean separation of concerns with multiple containers
- ✅ **Production Ready** - Error handling, logging, and environment configuration

## Available DataSuppliers

Provider ID **23862** provides access to 77 major automotive parts suppliers including:

### Top Suppliers by Article Count

| Rank | DataSupplier ID | Name | Articles |
|------|-----------------|------|----------|
| 1 | 206 | A.B.S. | 2,011,654 |
| 2 | 2 | BOSCH | 1,067,423 |
| 3 | 7 | SACHS | 526,098 |
| 4 | 8 | SWAG | 278,537 |
| 5 | 32 | CONTITECH | 197,577 |
| 6 | 12 | LEMFÖRDER | 177,379 |
| 7 | 14 | MEYLE | 100,570 |
| 8 | 3 | ATE | 14,158 |

[See complete list in datasuppliers.json](./data/datasuppliers.json)

## Installation

```bash
# Clone repository
git clone https://github.com/Motorlink/TECDOK-REPO.git
cd TECDOK-REPO

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TEC_PROVIDER_ID=23862
export TEC_API_KEY="your-api-key-here"
export TEC_COUNTRY="de"
export TEC_LANG="de"
```

## Quick Start

### Basic Usage

```python
from core_tecdoc_client import TecDocClient

# Initialize client
client = TecDocClient()

# Get all manufacturers
manufacturers = client.get_manufacturers()

# Get articles for a specific DataSupplier (e.g., ATE)
ate_articles = client.get_articles(data_supplier_id=3, page_size=100)
```

### Get Articles by DataSupplier

```python
# Get BOSCH articles
bosch_articles = client.get_articles(data_supplier_id=2, page_size=100)

# Get ATE articles
ate_articles = client.get_articles(data_supplier_id=3, page_size=100)

# Get articles for BMW from A.B.S.
bmw_abs_articles = client.get_articles(
    manufacturer_id=4,  # BMW
    data_supplier_id=206,  # A.B.S.
    page_size=100
)
```

## API Credentials

To use this API, you need:

1. **Provider ID**: 23862
2. **API Key**: Obtain from TecAlliance (sales.dach@tecalliance.net)
3. **Country**: DE (Germany)
4. **Language**: de (German)

## Project Structure

```
TECDOK-REPO/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── core_tecdoc_client.py             # Main API client
├── vin_lookup.py                     # VIN lookup module
├── article_vehicle_lookup.py         # Article-to-vehicle lookup
├── oe_cross_reference.py             # OE number cross-reference
├── examples/                         # Usage examples
│   ├── get_manufacturers.py
│   ├── get_articles_by_supplier.py
│   └── search_by_vin.py
├── data/                             # Reference data
│   ├── datasuppliers.json           # All 77 DataSuppliers
│   ├── manufacturers.json           # All 433 car manufacturers
│   └── countries.json               # Supported countries
└── tests/                            # Unit tests
    └── test_client.py
```

## API Endpoints

### Base URL

```
https://webservice.tecalliance.services/pegasus-3-0/services/TecdocToCatDLB.soapEndpoint
```

### Available Functions

- `getCountries` - Get supported countries
- `getManufacturers` - Get all car manufacturers
- `getArticles` - Get articles by various filters
- `getBrands` - Get parts brands
- `getVehicleByVIN` - Lookup vehicle by VIN (if supported)

## Authentication

The API uses **X-Api-Key** header authentication:

```xml
POST https://webservice.tecalliance.services/pegasus-3-0/services/TecdocToCatDLB.soapEndpoint

Headers:
  Content-Type: text/xml; charset=UTF-8
  X-Api-Key: your-api-key-here

Body:
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <getArticles xmlns="http://server.cat.tecdoc.net">
            <provider>23862</provider>
            <country>de</country>
            <lang>de</lang>
            <articleCountry>de</articleCountry>
            <dataSupplierIds>3</dataSupplierIds>
            <pageSize>100</pageSize>
            <pageNumber>0</pageNumber>
        </getArticles>
    </soap:Body>
</soap:Envelope>
```

## Examples

### Example 1: Get All Manufacturers

```python
from core_tecdoc_client import TecDocClient

client = TecDocClient()
manufacturers = client.get_manufacturers()

for mfg in manufacturers[:10]:
    print(f"{mfg['id']}: {mfg['name']}")
```

### Example 2: Get ATE Articles

```python
from core_tecdoc_client import TecDocClient

client = TecDocClient()
ate_articles = client.get_articles(data_supplier_id=3, page_size=20)

print(f"Total ATE articles: {ate_articles['total']}")
for article in ate_articles['articles'][:10]:
    print(f"{article['number']} - {article['name']}")
```

### Example 3: Search Articles for BMW

```python
from core_tecdoc_client import TecDocClient

client = TecDocClient()
bmw_articles = client.get_articles(manufacturer_id=4, page_size=100)

print(f"Total articles for BMW: {bmw_articles['total']}")
```

## Environment Variables

Create a `.env` file in the project root:

```bash
TEC_PROVIDER_ID=23862
TEC_API_KEY=your-api-key-here
TEC_COUNTRY=de
TEC_LANG=de
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_client.py -v
```

## Documentation

- [TecAlliance Official Documentation](https://www.tecalliance.net/)
- [API Reference](./docs/API_REFERENCE.md)
- [DataSuppliers List](./data/datasuppliers.json)
- [Manufacturers List](./data/manufacturers.json)

## Support

For API access and technical support:

- **Email**: sales.dach@tecalliance.net
- **Website**: https://www.tecalliance.net/
- **Phone**: +86 21 3387 0258

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Changelog

### Version 1.0.0 (2025-12-09)

- ✅ Initial release
- ✅ SOAP API client implementation
- ✅ Support for 77 DataSuppliers
- ✅ Support for 433 car manufacturers
- ✅ Complete documentation
- ✅ Example scripts

## Author

**Motorlink**
- Website: https://motorlink.de
- Email: info@motorlink.de

---

**Note**: This is a working implementation tested with Provider ID 23862 and valid API credentials from TecAlliance.
