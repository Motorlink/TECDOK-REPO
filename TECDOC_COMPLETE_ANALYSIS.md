# TECDOC API - VOLLSTÄNDIGE ANALYSE

## ZUSAMMENFASSUNG DER ERKENNTNISSE

### ✅ WAS WIR HABEN

**Provider ID:** 23862  
**API Key:** 2BeBXg6Nymr1VB3KjYRu69F4S9UGm24q5WUitw1bZKDBnePtCFtC  
**Endpoint:** https://webservice.tecalliance.services/pegasus-3-0/services/TecdocToCatDLB.soapEndpoint  
**Land:** DE (Deutschland)  
**Sprache:** de

---

## 📊 VERFÜGBARE DATEN ÜBER DIE API

### 1. Autohersteller (433 Stück)
**Funktion:** `getManufacturers`  
**Quelle:** Table 100 (Manufacturer)

**Beispiele:**
- AUDI (ID: 5)
- BMW (ID: 4)
- MERCEDES (ID: 38)
- VOLKSWAGEN (ID: 121)
- ... 429 weitere

**Datei:** `/home/ubuntu/TECDOK-REPO/reference_data/car_manufacturers_433.json`

---

### 2. Teile-Hersteller / DataSuppliers (77 Stück)
**Funktion:** `getArticles` (indirekt)  
**Quelle:** Table 040 (Data Supplier)

**Top 10:**
1. A.B.S. (ID: 206) - 2.011.654 Artikel
2. BOSCH (ID: 2) - 1.067.423 Artikel
3. SACHS (ID: 7) - 526.098 Artikel
4. SWAG (ID: 8) - 278.537 Artikel
5. CONTITECH (ID: 32) - 197.577 Artikel
6. LEMFÖRDER (ID: 12) - 177.379 Artikel
7. MEYLE (ID: 14) - 100.570 Artikel
8. CORTECO (ID: 30) - 97.319 Artikel
9. FEBI BILSTEIN (ID: 29) - 92.820 Artikel
10. ELRING (ID: 10) - 20.606 Artikel

**Datei:** `/home/ubuntu/TECDOK-REPO/reference_data/parts_manufacturers_77.json`

---

### 3. Artikellisten (nur 4 Felder!)
**Funktion:** `getArticles`  
**Quelle:** Table 200 (Article Table)

**Verfügbare Felder:**
- `articleNumber` - Artikelnummer
- `mfrId` - Hersteller-ID
- `mfrName` - Hersteller-Name
- `dataSupplierId` - DataSupplier-ID

**NICHT verfügbar:**
- ❌ EAN-Nummer
- ❌ Beschreibung
- ❌ Produktbilder
- ❌ OE-Nummern
- ❌ Fahrzeugzuordnungen
- ❌ Preise
- ❌ Technische Daten

---

### 4. Länder
**Funktion:** `getCountries`  
**Quelle:** Table 010 (Country Table)

**Beispiel:** Deutschland (DE)

---

## ❌ NICHT VERFÜGBARE DATEN

### Fehlende Tabellen in der API:

| Tabelle | Name | Inhalt | Status |
|---------|------|--------|--------|
| **203** | Reference Numbers | **OE-Nummern!** | ❌ Nicht verfügbar |
| **209** | GTIN | **EAN-Codes!** | ❌ Nicht verfügbar |
| **231** | Graphics / Documents | **Produktbilder!** | ❌ Nicht verfügbar |
| **232** | Allocation of Graphics | Bild-Zuordnung | ❌ Nicht verfügbar |
| **400** | Article Linkage | **Fahrzeug-Zuordnung!** | ❌ Nicht verfügbar |
| **120** | Vehicle Types | KTypNo (Fahrzeugtypen) | ❌ Nicht verfügbar |
| **201** | Price Information | Preise | ❌ Nicht verfügbar |
| **206** | Article Information | Beschreibungen | ❌ Nicht verfügbar |
| **210** | Article Criteria | Technische Daten | ❌ Nicht verfügbar |

---

## 🔍 WIE TECDOC FUNKTIONIERT (laut Dokumentation)

### Datenfluss: Artikel → Fahrzeug

```
1. ARTIKEL (Table 200)
   ↓ ArtNo
2. GENERIC ARTICLE ALLOCATION (Table 211)
   ↓ GenArtNo
3. ARTICLE LINKAGE (Table 400) ← KRITISCH!
   ↓ LnkTargetNo (= KTypNo)
4. VEHICLE TYPES (Table 120)
   ↓ ManNo
5. MANUFACTURER (Table 100)
```

### Beispiel:

**Artikel:** HU 7029 z (MANN-FILTER Ölfilter)  
↓  
**Generic Article:** 320 (Ölfilter-Kategorie)  
↓  
**Linkage Target:** KTypNo 12345 (z.B. Audi A4 3.2 FSI 2005)  
↓  
**Manufacturer:** 5 (Audi)

**PROBLEM:** Table 400 (Article Linkage) ist über unsere API NICHT verfügbar!

---

## 📋 ALLE TECDOC TABELLEN (119 Stück)

### Referenzdaten (001-053)
- 001 Header
- 005 Reference Data Announcements
- 010 Country Table
- 012 Country and Language-dependent Descriptions
- 020 Language
- 030 Language Descriptions
- 031 Language Descriptions for Article Criteria (Logistics)
- 035 Text Modules
- 040 Data Supplier Main Address
- 042 Data Supplier Logos
- 043 Data Supplier Addresses
- 050 Criteria Table
- 051 Key Tables
- 052 Key Table Entries
- 053 Criteria Table (Logistics)

### Fahrzeuge & Hersteller (100-180)
- 100 Manufacturer
- 103 Manufacturer-KBA Reference
- 110 Vehicle Model Series
- 115 Linkage Target Types
- 120 Vehicle Types (KTypNo!)
- 121-129 Various vehicle type allocations
- 140-147 Additional vehicle descriptions
- 155-156 Engines
- 160-164 Axle information
- 180 Engine output and performance

### Artikel & Produkte (200-233)
- 200 Article Table
- 201 Price Information
- 202 Article Country Restrictions
- 203 Reference Numbers (OE!)
- 204 Superseding Articles
- 205 Parts Lists
- 206 Article Information
- 207 Trade Numbers
- 208 Parts List Criteria
- 209 GTIN (EAN!)
- 210 Article Criteria
- 211 Article to Generic Article Allocation
- 212 Country-Specific Article-data
- 213 Article Criteria (Logistics)
- 214 Article Packaging Items
- 215 Parts Lists Country Restrictions
- 216 Article Packaging Items – Country Restrictions
- 217 Allocation of Parts-List-Coordinates
- 218 Packaging Items Lot Sizes
- 222 Accessory lists
- 228 Accessory Lists Criteria
- 231 Graphics / Documents (Images!)
- 232 Allocation of Graphics to Article Numbers
- 233 Context Sensitive Graphics

### Generische Artikel & Suche (301-340)
- 301 TecDoc Search Structure
- 302 Allocation of GenArt to Search Structure
- 304 Allocation of Criteria to Search Structure
- 305 Quick-start Icons
- 306-307 Icon allocations
- 320 Generic Articles
- 323 Standardised Article Description
- 324 Assembly Groups
- 325 Purpose of Use
- 327 Generic Article Synonyms
- 328 Mandatory Criteria
- 329 Proposed Criteria
- 330-335 Criteria allocations
- 340 DQM Permissions

### Artikel-Verknüpfungen (400-432)
- 400 Article Linkage (Fahrzeug-Zuordnung!)
- 401 Search Information Texts
- 403 Country restriction of linkage
- 404 Sorting of linkage
- 410 Linkage attributes
- 432 Linkage-dependent Graphics/Documents

### Nutzfahrzeuge (532-555)
- 532-555 Commercial vehicle tables

### Datenhandbuch (900-990)
- 900 TecDoc data guide
- 990 TecDoc data guide – Terms and Documents

---

## 💡 LÖSUNGSOPTIONEN

### Option 1: API-Upgrade anfordern
**Kontakt:** TecAlliance Sales (sales.dach@tecalliance.net)

**Anfrage:**
- Zugriff auf Table 400 (Article Linkage)
- Zugriff auf Table 203 (OE Numbers)
- Zugriff auf Table 209 (GTIN/EAN)
- Zugriff auf Table 231/232 (Images)
- Zugriff auf Table 120 (Vehicle Types)

### Option 2: TAF-Dateien importieren
**Vorteile:**
- Vollständiger Datenzugriff
- Eigene Datenbank
- Keine API-Limits

**Nachteile:**
- Hoher Implementierungsaufwand
- Regelmäßige Updates erforderlich
- Speicherplatz-Bedarf

### Option 3: TecDoc Katalog-Software
**Vorteile:**
- Fertige Lösung
- Vollständiger Datenzugriff
- Support von TecAlliance

**Nachteile:**
- Lizenzkosten
- Weniger Flexibilität

---

## 📁 GESPEICHERTE DATEIEN

### GitHub Repository: TECDOK-REPO
**URL:** https://github.com/Motorlink/TECDOK-REPO

**Struktur:**
```
TECDOK-REPO/
├── reference_data/
│   ├── car_manufacturers_433.json
│   ├── parts_manufacturers_77.json
│   ├── parts_manufacturers_77.csv
│   └── README.md
├── data/
│   ├── datasuppliers.json
│   ├── manufacturers.json
│   └── countries.json
├── examples/
│   ├── get_manufacturers.py
│   └── get_articles_by_supplier.py
├── core_tecdoc_client.py
├── requirements.txt
├── .env.example
└── README.md
```

### Lokale Analyse-Dateien
- `/home/ubuntu/TecDoc-Data-Format.pdf` (207 Seiten)
- `/home/ubuntu/tecdoc_all_tables.txt` (119 Tabellen)
- `/home/ubuntu/tecdoc_article_tables_analysis.md` (Detaillierte Analyse)
- `/home/ubuntu/documentation_analysis.md` (Dokumentations-Übersicht)

---

## 🎯 FAZIT

### Was funktioniert:
✅ Autohersteller-Liste abrufen  
✅ Teile-Hersteller-Liste abrufen  
✅ Artikelnummern-Listen abrufen (nur 4 Felder)  
✅ Länder-Liste abrufen

### Was NICHT funktioniert:
❌ Fahrzeugzuordnung zu Artikeln  
❌ OE-Nummern abrufen  
❌ EAN-Codes abrufen  
❌ Produktbilder abrufen  
❌ Beschreibungen abrufen  
❌ Technische Daten abrufen  
❌ Preise abrufen

### Empfehlung:
**Kontaktieren Sie TecAlliance für einen API-Upgrade oder TAF-Datei-Zugang!**

Die aktuelle API (Provider 23862) ist für Ihre Anforderungen zu limitiert.
