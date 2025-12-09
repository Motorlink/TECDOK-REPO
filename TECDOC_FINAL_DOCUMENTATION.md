# TecDoc API - Vollständige Dokumentation (Provider ID 23862)

**Datum:** 09. Dezember 2025  
**Autor:** Manus AI

---

## 1. ZUSAMMENFASSUNG

Diese Dokumentation beschreibt den **tatsächlichen Funktionsumfang** der TecDoc API mit Ihrer Lizenz (Provider ID 23862). Die Analyse hat ergeben, dass der Zugang **stark limitiert** ist und die meisten erwarteten Funktionen **nicht verfügbar** sind.

| Eigenschaft | Status |
|---|---|
| **API-Typ** | SOAP (nicht JSON) |
| **Funktionierende Funktionen** | 3 |
| **Nicht verfügbare Funktionen** | 30+ |
| **Fahrzeug-Verknüpfung** | ❌ Nicht möglich |
| **OE-Nummern-Suche** | ❌ Nicht möglich |
| **EAN / Bilder / Beschreibungen** | ❌ Nicht möglich |

---

## 2. FUNKTIONIERENDE API-FUNKTIONEN (3)

### 2.1. `getManufacturers`

Ruft eine Liste aller **Autohersteller** ab.

**Request (SOAP):**
```xml
<getManufacturers xmlns="http://server.cat.tecdoc.net">
    <provider>23862</provider>
    <country>de</country>
    <lang>de</lang>
</getManufacturers>
```

**Response (Beispiel):**
```xml
<data>
    <array>
        <id>5</id>
        <name>AUDI</name>
    </array>
    <array>
        <id>4</id>
        <name>BMW</name>
    </array>
</data>
```

**Ergebnis:** ✅ Liefert **433 Autohersteller**.

### 2.2. `getArticles`

Ruft eine **reine Artikelnummern-Liste** ab, gefiltert nach Teile-Hersteller (DataSupplier).

**Request (SOAP):**
```xml
<getArticles xmlns="http://server.cat.tecdoc.net">
    <provider>23862</provider>
    <country>de</country>
    <lang>de</lang>
    <articleCountry>de</articleCountry>
    <dataSupplierIds>4</dataSupplierIds> <!-- 4 = MANN-FILTER -->
</getArticles>
```

**Response (Beispiel):**
```xml
<articles>
    <dataSupplierId>4</dataSupplierId>
    <articleNumber>1180461S01</articleNumber>
    <mfrId>504</mfrId>
    <mfrName>MANN-FILTER</mfrName>
</articles>
```

**Ergebnis:** ✅ Liefert nur **4 Felder** pro Artikel. Keine EAN, Bilder, OE-Nummern oder Fahrzeugzuordnungen.

### 2.3. `getCountries`

Ruft eine Liste der verfügbaren Länder ab.

**Request (SOAP):**
```xml
<getCountries xmlns="http://server.cat.tecdoc.net">
    <provider>23862</provider>
</getCountries>
```

**Response (Beispiel):**
```xml
<data>
    <array>
        <countryCode>DE</countryCode>
        <countryName>Deutschland</countryName>
    </array>
</data>
```

**Ergebnis:** ✅ Funktioniert.

---

## 3. NICHT VERFÜGBARE FUNKTIONEN (Vergleich mit `Pasted_content.txt`)

Die in `Pasted_content.txt` beschriebenen Funktionen sind mit Ihrer Lizenz **NICHT VERFÜGBAR**.

| Funktion (aus `Pasted_content.txt`) | Status | API-Antwort |
|---|---|---|
| `getBrands` | ⚠️ **FEHLER** | `Unbekannt` (kein "Unknown Call") |
| `getArticlesDirectSearchAllNumbers4` | ❌ **NICHT VERFÜGBAR** | `Unknown Call` |
| `getLinkageTargetsByArticleId` | ❌ **NICHT VERFÜGBAR** | `Unknown Call` |
| `getVehicleIdsByVIN` | ❌ **NICHT VERFÜGBAR** | `Unknown Call` |
| `getLinkageTargetDetails2` | ❌ **NICHT VERFÜGBAR** | `Unknown Call` |
| `getModelSeries` | ❌ **NICHT VERFÜGBAR** | `Unknown Call` |
| `getVehiclesByModelSeries` | ❌ **NICHT VERFÜGBAR** | `Unknown Call` |

---

## 4. FAZIT & EMPFEHLUNG

**Ihre API-Lizenz (Provider 23862) ist extrem limitiert.** Sie können nur Basis-Listen abrufen, aber keine detaillierten Informationen oder Verknüpfungen zwischen Fahrzeugen und Artikeln.

**Um die gewünschten Daten zu erhalten, benötigen Sie:**

1.  **API-Upgrade:** Bitten Sie TecAlliance um eine Lizenz mit vollem Funktionsumfang.
2.  **TAF-Dateien:** Importieren Sie die TecDoc-Datenpakete direkt in Ihre eigene Datenbank.
3.  **TecDoc Katalog-Software:** Nutzen Sie eine fertige Kataloglösung von TecAlliance.

Die `Pasted_content.txt` beschreibt eine **erweiterte API-Version**, auf die Sie **keinen Zugriff** haben.md**inen Zugriff haben. Die Diskrepanz liegt in der **Lizenz**, nicht in der technischen Umsetzung.
