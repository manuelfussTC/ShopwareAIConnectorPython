
# Shopware AI Connector

Der Shopware AI Connector ist ein fortschrittliches Tool, das die Kraft der generativen KI nutzt, um die Interaktion mit der Shopware-API durch natürlichsprachliche Anfragen zu ermöglichen. Es transformiert einfache, menschliche Anfragen in präzise API-Aufrufe, wodurch die Notwendigkeit entfällt, spezifische Funktionen manuell zu schreiben. Dieses Tool ist ideal für Shopware-Benutzer, die eine effizientere und benutzerfreundlichere Methode zur Datenabfrage und -manipulation suchen.

## Features

- **Natürlichsprachliche Anfragen:** Verarbeite Anfragen in natürlicher Sprache und finde die entsprechenden Shopware-API-Endpunkte.
- **Automatische Generierung von API-Funktionen:** Die Funktionen werden automatisch aus der Shopware-API-Dokumentation generiert.
- **Unterstützung für Diverse Anfragen:** Fähig, eine Vielzahl von Anfragen zu verarbeiten, von einfachen Abfragen bis hin zu komplexeren Anforderungen.

## Installation

Voraussetzungen:
- Python 3.10
- PHP 7.4 oder höher
- Zugang zur Shopware-API
- OpenAI API-Schlüssel

### Schritte zur Installation:

1. **Klone das Repository:**
   ```
   git clone https://github.com/your-repository/shopware-ai-connector.git
   cd shopware-ai-connector
   ```

2. **Installiere die erforderlichen Pakete:**
   ```
   pip install -r requirements.txt
   ```

3. **Konfiguriere deine .env Datei und die Konfigurationsdatei:**
   - Füge deinen OpenAI API-Schlüssel und Shopware-API-Zugangsinformationen in die .env Datei ein.
   - Fülle die `config_example.json` Datei mit den erforderlichen Informationen und benenne sie um in `config.json`.

4. **Führe die initialen Skripte aus:**
   - PHP-Skript zur Generierung von Embeddings
   - Python-Skript zur Einrichtung

## Benutzung

1. **Starte das Hauptprogramm:**
   ```
   python main.py
   ```

2. **Gib eine natürlichsprachliche Anfrage ein:**
   Zum Beispiel: "Zeige alle Artikel in meinem Shop mit Name, Preis und Artikelnummer, Limit 4".

3. **Erhalte die Ergebnisse:**
   Das System verarbeitet deine Anfrage und zeigt die entsprechenden Ergebnisse an.

## Beitrag

Beiträge sind willkommen! Wenn du eine Idee zur Verbesserung hast, zögere nicht, ein Issue zu eröffnen oder einen Pull Request zu machen.

## Lizenz

[MIT](https://choosealicense.com/licenses/mit/)

## Kontakt

Für Fragen oder Unterstützung kannst du mich unter [deine-email@example.com](mailto:deine-email@example.com) erreichen.
