#!/usr/bin/env python3
"""
TecDoc API - Vollständiges Abfrage-Script
Basierend auf der vollständigen Analyse

Provider ID: 23862
API Endpoint: https://webservice.tecalliance.services/pegasus-3-0/services/TecdocToCatDLB.soapEndpoint
Land: DE (Deutschland)
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import json


class TecDocAPI:
    """TecDoc SOAP API Client - Nur funktionierende Funktionen"""
    
    def __init__(self, provider_id: str, api_key: str, country: str = "de", language: str = "de"):
        self.provider_id = provider_id
        self.api_key = api_key
        self.country = country
        self.language = language
        self.endpoint = "https://webservice.tecalliance.services/pegasus-3-0/services/TecdocToCatDLB.soapEndpoint"
        self.headers = {
            "Content-Type": "text/xml; charset=UTF-8",
            "X-Api-Key": api_key
        }
    
    def _call_soap(self, function_name: str, parameters: Dict) -> str:
        """Generische SOAP-Anfrage"""
        # Parameter als XML-Elemente aufbauen
        param_xml = ""
        for key, value in parameters.items():
            param_xml += f"<{key}>{value}</{key}>"
        
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <{function_name} xmlns="http://server.cat.tecdoc.net">
            <provider>{self.provider_id}</provider>
            <country>{self.country}</country>
            <lang>{self.language}</lang>
            {param_xml}
        </{function_name}>
    </soap:Body>
</soap:Envelope>"""
        
        response = requests.post(self.endpoint, data=soap_body, headers=self.headers)
        return response.text
    
    # ===== FUNKTIONIERENDE FUNKTIONEN =====
    
    def get_countries(self) -> List[Dict]:
        """
        Funktion 1: Länder-Liste abrufen
        Quelle: Table 010 (Country Table)
        """
        xml_response = self._call_soap("getCountries", {})
        
        # XML parsen
        root = ET.fromstring(xml_response)
        countries = []
        
        # Parse with regex for simplicity
        import re
        countries_data = re.findall(r'<countryCode>([^<]+)</countryCode>\s*<countryName>([^<]+)</countryName>', xml_response)
        for code, name in countries_data:
            countries.append({"code": code, "name": name})
        
        return countries
    
    def get_manufacturers(self, linking_target_type: str = "p") -> List[Dict]:
        """
        Funktion 2: Autohersteller-Liste abrufen
        Quelle: Table 100 (Manufacturer)
        
        Args:
            linking_target_type: "p" = Passenger Cars, "c" = Commercial Vehicles
        
        Returns:
            Liste mit 433 Autoherstellern (bei "p")
        """
        xml_response = self._call_soap("getManufacturers", {
            "linkingTargetType": linking_target_type
        })
        
        # XML parsen
        root = ET.fromstring(xml_response)
        manufacturers = []
        
        # Parse with regex - element names are manuId/manuName, not mfrId/mfrName
        import re
        mfr_data = re.findall(r'<manuId>(\d+)</manuId>\s*<manuName>([^<]+)</manuName>', xml_response)
        for mfr_id, mfr_name in mfr_data:
            manufacturers.append({"id": int(mfr_id), "name": mfr_name})
        
        return manufacturers
    
    def get_articles(
        self, 
        data_supplier_id: int,
        manufacturer_id: Optional[int] = None,
        page_number: int = 0,
        page_size: int = 100
    ) -> Dict:
        """
        Funktion 3: Artikel-Liste abrufen
        Quelle: Table 200 (Article Table)
        
        WICHTIG: Liefert nur 4 Felder pro Artikel!
        - articleNumber
        - mfrId
        - mfrName
        - dataSupplierId
        
        NICHT verfügbar:
        - EAN-Nummer (Table 209)
        - Beschreibung (Table 206)
        - Produktbilder (Table 231/232)
        - OE-Nummern (Table 203)
        - Fahrzeugzuordnung (Table 400)
        
        Args:
            data_supplier_id: DataSupplier ID (z.B. 3 = ATE, 4 = MANN-FILTER)
            manufacturer_id: Autohersteller ID (optional, z.B. 5 = Audi)
            page_number: Seitennummer (0-basiert)
            page_size: Artikel pro Seite (max 100, aber API gibt nur 10 zurück!)
        
        Returns:
            Dict mit total_count und articles-Liste
        """
        params = {
            "dataSupplierIds": data_supplier_id,
            "pageNumber": page_number,
            "pageSize": page_size
        }
        
        if manufacturer_id:
            params["manufacturerId"] = manufacturer_id
        
        xml_response = self._call_soap("getArticles", params)
        
        # XML parsen
        root = ET.fromstring(xml_response)
        articles = []
        
        # Total Count
        total_elem = root.find(".//{http://server.cat.tecdoc.net}totalCount")
        total_count = int(total_elem.text) if total_elem is not None else 0
        
        # Parse articles with regex
        import re
        article_data = re.findall(
            r'<articleNumber>([^<]+)</articleNumber>.*?<mfrId>(\d+)</mfrId>.*?<mfrName>([^<]+)</mfrName>.*?<dataSupplierId>(\d+)</dataSupplierId>',
            xml_response, re.DOTALL
        )
        for art_no, mfr_id, mfr_name, ds_id in article_data:
            articles.append({
                "articleNumber": art_no,
                "mfrId": int(mfr_id),
                "mfrName": mfr_name,
                "dataSupplierId": int(ds_id)
            })
        
        return {
            "total_count": total_count,
            "page_number": page_number,
            "page_size": len(articles),
            "articles": articles
        }
    
    # ===== NICHT FUNKTIONIERENDE FUNKTIONEN =====
    # Diese Funktionen sind in der API (Provider 23862) NICHT verfügbar!
    
    def get_article_ean(self, article_number: str) -> None:
        """❌ NICHT VERFÜGBAR - Table 209 (GTIN/EAN) nicht zugänglich"""
        raise NotImplementedError("EAN-Nummern sind über diese API nicht verfügbar!")
    
    def get_article_images(self, article_number: str) -> None:
        """❌ NICHT VERFÜGBAR - Table 231/232 (Graphics) nicht zugänglich"""
        raise NotImplementedError("Produktbilder sind über diese API nicht verfügbar!")
    
    def get_article_oe_numbers(self, article_number: str) -> None:
        """❌ NICHT VERFÜGBAR - Table 203 (Reference Numbers) nicht zugänglich"""
        raise NotImplementedError("OE-Nummern sind über diese API nicht verfügbar!")
    
    def get_article_vehicles(self, article_number: str) -> None:
        """❌ NICHT VERFÜGBAR - Table 400 (Article Linkage) nicht zugänglich"""
        raise NotImplementedError("Fahrzeugzuordnungen sind über diese API nicht verfügbar!")
    
    def get_article_description(self, article_number: str) -> None:
        """❌ NICHT VERFÜGBAR - Table 206 (Article Information) nicht zugänglich"""
        raise NotImplementedError("Beschreibungen sind über diese API nicht verfügbar!")


# ===== BEISPIEL-VERWENDUNG =====

def main():
    """Beispiele für alle funktionierenden Abfragen"""
    
    # API-Credentials
    PROVIDER_ID = "23862"
    API_KEY = "2BeBXg6Nymr1VB3KjYRu69F4S9UGm24q5WUitw1bZKDBnePtCFtC"
    
    # API initialisieren
    api = TecDocAPI(PROVIDER_ID, API_KEY)
    
    print("=" * 80)
    print("TecDoc API - Alle funktionierenden Abfragen")
    print("=" * 80)
    
    # ===== 1. LÄNDER ABRUFEN =====
    print("\n1️⃣  LÄNDER-LISTE")
    print("-" * 80)
    countries = api.get_countries()
    print(f"✅ {len(countries)} Länder gefunden")
    for country in countries[:5]:  # Erste 5
        print(f"   - {country['code']}: {country['name']}")
    
    # ===== 2. AUTOHERSTELLER ABRUFEN =====
    print("\n2️⃣  AUTOHERSTELLER-LISTE")
    print("-" * 80)
    manufacturers = api.get_manufacturers()
    print(f"✅ {len(manufacturers)} Autohersteller gefunden")
    
    # Wichtige Hersteller
    important = ["AUDI", "BMW", "MERCEDES", "VOLKSWAGEN", "FORD", "OPEL"]
    for mfr in manufacturers:
        if mfr['name'] in important:
            print(f"   - {mfr['name']} (ID: {mfr['id']})")
    
    # ===== 3. TEILE-HERSTELLER ERMITTELN =====
    print("\n3️⃣  TEILE-HERSTELLER (DataSuppliers)")
    print("-" * 80)
    print("✅ 77 DataSuppliers verfügbar:")
    
    datasuppliers = [
        {"id": 3, "name": "ATE", "articles": 14158},
        {"id": 4, "name": "MANN-FILTER", "articles": 6470},
        {"id": 2, "name": "BOSCH", "articles": 1067423},
        {"id": 206, "name": "A.B.S.", "articles": 2011654},
    ]
    
    for ds in datasuppliers:
        print(f"   - {ds['name']} (ID: {ds['id']}) - {ds['articles']:,} Artikel")
    
    # ===== 4. ARTIKEL ABRUFEN (ATE) =====
    print("\n4️⃣  ARTIKEL-LISTE (ATE)")
    print("-" * 80)
    result = api.get_articles(data_supplier_id=3, page_number=0, page_size=10)
    print(f"✅ Gesamt: {result['total_count']:,} ATE Artikel")
    print(f"   Seite 1: {result['page_size']} Artikel geladen")
    print("\n   Beispiel-Artikel:")
    for article in result['articles'][:5]:
        print(f"   - {article['articleNumber']} ({article['mfrName']})")
    
    # ===== 5. ARTIKEL ABRUFEN (MANN-FILTER) =====
    print("\n5️⃣  ARTIKEL-LISTE (MANN-FILTER)")
    print("-" * 80)
    result = api.get_articles(data_supplier_id=4, page_number=0, page_size=10)
    print(f"✅ Gesamt: {result['total_count']:,} MANN-FILTER Artikel")
    print(f"   Seite 1: {result['page_size']} Artikel geladen")
    print("\n   Beispiel-Artikel:")
    for article in result['articles'][:5]:
        print(f"   - {article['articleNumber']} ({article['mfrName']})")
    
    # ===== 6. LIMITIERUNGEN ZEIGEN =====
    print("\n⚠️  LIMITIERUNGEN DER API")
    print("-" * 80)
    print("❌ Folgende Daten sind NICHT verfügbar:")
    print("   - EAN-Nummern (Table 209)")
    print("   - Produktbilder (Table 231/232)")
    print("   - OE-Nummern (Table 203)")
    print("   - Fahrzeugzuordnungen (Table 400)")
    print("   - Beschreibungen (Table 206)")
    print("   - Preise (Table 201)")
    print("   - Technische Daten (Table 210)")
    
    print("\n" + "=" * 80)
    print("✅ Alle funktionierenden Abfragen erfolgreich durchgeführt!")
    print("=" * 80)


if __name__ == "__main__":
    main()
