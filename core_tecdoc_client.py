"""
TecDoc API Core Client
======================

Main client for TecAlliance TecDoc Web Service API (Pegasus 3.0).
Handles SOAP requests, authentication, and error handling.

Provider ID: 23862
Country: DE (Germany)
Language: de (German)
"""

import os
import logging
import re
from typing import Any, Dict, List, Optional
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TecDocClient:
    """
    TecDoc API Client for automotive parts data.
    
    Supports:
    - 77 DataSuppliers (parts manufacturers)
    - 433 Car Manufacturers
    - Over 3 million articles
    """
    
    SOAP_ENDPOINT = "https://webservice.tecalliance.services/pegasus-3-0/services/TecdocToCatDLB.soapEndpoint"
    
    def __init__(
        self,
        provider_id: Optional[int] = None,
        api_key: Optional[str] = None,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        timeout: int = 30
    ) -> None:
        """
        Initialize TecDoc API client.
        
        Args:
            provider_id: TecDoc provider ID (default: from TEC_PROVIDER_ID env)
            api_key: API authentication key (default: from TEC_API_KEY env)
            country: Country code (default: from TEC_COUNTRY env or "de")
            lang: Language code (default: from TEC_LANG env or "de")
            timeout: Request timeout in seconds (default: 30)
        """
        self.provider_id = provider_id or int(os.getenv("TEC_PROVIDER_ID", "23862"))
        self.api_key = api_key or os.getenv("TEC_API_KEY", "")
        self.country = (country or os.getenv("TEC_COUNTRY", "de")).lower()
        self.lang = (lang or os.getenv("TEC_LANG", "de")).lower()
        self.timeout = timeout
        
        if not self.provider_id or not self.api_key:
            raise ValueError("TecDocClient: Provider ID and API Key are required")
        
        # Mask API key for logging
        masked_key = f"{self.api_key[:4]}...{self.api_key[-4:]}" if len(self.api_key) > 8 else "***"
        logger.info(
            f"TecDocClient initialized (provider={self.provider_id}, country={self.country}, "
            f"lang={self.lang}, key={masked_key})"
        )
    
    def _build_soap_request(self, function: str, params: Dict[str, Any]) -> str:
        """
        Build SOAP XML request body.
        
        Args:
            function: TecDoc function name (e.g., "getArticles")
            params: Function parameters
            
        Returns:
            SOAP XML string
        """
        # Build parameter XML
        param_xml = f"""
            <provider>{self.provider_id}</provider>
            <country>{self.country}</country>
            <lang>{self.lang}</lang>
        """
        
        for key, value in params.items():
            if value is not None:
                param_xml += f"            <{key}>{value}</{key}>\n"
        
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <{function} xmlns="http://server.cat.tecdoc.net">
{param_xml.rstrip()}
        </{function}>
    </soap:Body>
</soap:Envelope>"""
        
        return soap_body
    
    def _call_soap(self, function: str, params: Dict[str, Any]) -> str:
        """
        Make SOAP API call.
        
        Args:
            function: TecDoc function name
            params: Function parameters
            
        Returns:
            Raw XML response
            
        Raises:
            requests.RequestException: On network errors
            requests.HTTPError: On HTTP errors
        """
        soap_body = self._build_soap_request(function, params)
        
        headers = {
            "Content-Type": "text/xml; charset=UTF-8",
            "X-Api-Key": self.api_key,
        }
        
        try:
            response = requests.post(
                self.SOAP_ENDPOINT,
                data=soap_body,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            logger.error(f"TecDoc API RequestException: {exc}")
            raise
        
        if not response.ok:
            logger.error(
                f"TecDoc API Error: HTTP {response.status_code} - {response.text[:500]}"
            )
            response.raise_for_status()
        
        return response.text
    
    def get_countries(self) -> List[Dict[str, str]]:
        """
        Get list of supported countries.
        
        Returns:
            List of countries with code and name
        """
        xml_response = self._call_soap("getCountries", {})
        
        # Parse XML response
        country_codes = re.findall(r'<countryCode>([^<]+)</countryCode>', xml_response)
        country_names = re.findall(r'<countryName>([^<]+)</countryName>', xml_response)
        
        countries = []
        for code, name in zip(country_codes, country_names):
            countries.append({"code": code, "name": name})
        
        logger.info(f"Retrieved {len(countries)} countries")
        return countries
    
    def get_manufacturers(self, linking_target_type: str = "p") -> List[Dict[str, str]]:
        """
        Get list of all car manufacturers.
        
        Args:
            linking_target_type: Target type ("p" for passenger cars)
            
        Returns:
            List of manufacturers with ID and name
        """
        params = {"linkingTargetType": linking_target_type}
        xml_response = self._call_soap("getManufacturers", params)
        
        # Parse XML response
        manu_ids = re.findall(r'<manuId>(\d+)</manuId>', xml_response)
        manu_names = re.findall(r'<manuName>([^<]+)</manuName>', xml_response)
        
        manufacturers = []
        for mid, name in zip(manu_ids, manu_names):
            manufacturers.append({"id": mid, "name": name})
        
        logger.info(f"Retrieved {len(manufacturers)} manufacturers")
        return manufacturers
    
    def get_articles(
        self,
        data_supplier_id: Optional[int] = None,
        manufacturer_id: Optional[int] = None,
        article_country: Optional[str] = None,
        page_size: int = 100,
        page_number: int = 0
    ) -> Dict[str, Any]:
        """
        Get articles (parts) with optional filters.
        
        Args:
            data_supplier_id: Filter by parts supplier (e.g., 3 for ATE, 2 for BOSCH)
            manufacturer_id: Filter by car manufacturer (e.g., 4 for BMW)
            article_country: Article country code (default: same as client country)
            page_size: Number of results per page (max 100)
            page_number: Page number (0-based)
            
        Returns:
            Dict with total count and list of articles
        """
        params = {
            "articleCountry": article_country or self.country,
            "pageSize": page_size,
            "pageNumber": page_number,
        }
        
        if data_supplier_id:
            params["dataSupplierIds"] = data_supplier_id
        
        if manufacturer_id:
            params["manufacturerId"] = manufacturer_id
        
        xml_response = self._call_soap("getArticles", params)
        
        # Parse XML response
        total_match = re.search(r'<totalMatchingArticles>(\d+)</totalMatchingArticles>', xml_response)
        total = int(total_match.group(1)) if total_match else 0
        
        # Extract articles
        article_numbers = re.findall(r'<articleNumber>([^<]+)</articleNumber>', xml_response)
        mfr_ids = re.findall(r'<mfrId>(\d+)</mfrId>', xml_response)
        mfr_names = re.findall(r'<mfrName>([^<]+)</mfrName>', xml_response)
        
        articles = []
        for artnum, mfr_id, mfr_name in zip(article_numbers, mfr_ids, mfr_names):
            articles.append({
                "number": artnum,
                "manufacturer_id": mfr_id,
                "manufacturer_name": mfr_name
            })
        
        logger.info(
            f"Retrieved {len(articles)} articles (total: {total}, page: {page_number})"
        )
        
        return {
            "total": total,
            "page": page_number,
            "page_size": page_size,
            "articles": articles
        }
    
    def get_raw_response(self, function: str, params: Dict[str, Any]) -> str:
        """
        Get raw XML response for any function.
        
        Args:
            function: TecDoc function name
            params: Function parameters
            
        Returns:
            Raw XML response string
        """
        return self._call_soap(function, params)


if __name__ == "__main__":
    # Example usage
    client = TecDocClient()
    
    # Get countries
    print("\n=== Countries ===")
    countries = client.get_countries()
    for country in countries:
        print(f"  {country['code']}: {country['name']}")
    
    # Get manufacturers
    print("\n=== Manufacturers (first 10) ===")
    manufacturers = client.get_manufacturers()
    for mfg in manufacturers[:10]:
        print(f"  {mfg['id']}: {mfg['name']}")
    
    # Get ATE articles
    print("\n=== ATE Articles (first 10) ===")
    ate_articles = client.get_articles(data_supplier_id=3, page_size=10)
    print(f"Total ATE articles: {ate_articles['total']}")
    for article in ate_articles['articles']:
        print(f"  {article['number']} - {article['manufacturer_name']}")
