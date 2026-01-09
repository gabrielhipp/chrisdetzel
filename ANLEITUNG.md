# Chrisdetzel - Kurzanleitung

Willkommen! Diese Anleitung zeigt dir, wie du das Projekt nutzt.

## Vorbereitung

1. **Excel-Datei lokal speichern**
   - Speichere deine Excel-Datei (`Preisanalyse Wettbewerber v2.1.xlsx`) irgendwo auf deinem Computer
   - Merke dir den vollständigen Pfad zur Datei

2. **Repository öffnen**
   - Öffne den Chrisdetzel-Ordner in VS Code

## Verwendung

1. **Pfad eintragen**
   - Öffne die Datei `chrisdetzel.ipynb` (das Notebook)
   - In der 2. Zelle findest du die Zeile mit `path = '...'`
   - Ersetze den Pfad mit dem Pfad zu deiner Excel-Datei

   Beispiel:
   ```python
   path = '/Users/dein_name/Documents/Preisanalyse Wettbewerber v2.1.xlsx'
   ```

2. **Notebook ausführen**
   - Führe jede Zelle nacheinander aus (oben rechts auf den "Play"-Button klicken)
   - Lass jede Zelle fertig werden, bevor du zur nächsten gehst
   - Das Programm öffnet automatisch Chrome und scrapped die Daten

## Optional: Headless Mode aktivieren

Wenn du möchtest, dass Chrome im Hintergrund läuft (unsichtbar):

- Öffne die 1. Zelle mit dem Code
- Finde die Zeile `#options.add_argument("--headless")`
- Entferne das `#` davor, sodass es `options.add_argument("--headless")` heißt
- Das war's! Chrome läuft jetzt im Hintergrund

## Fertig

Die neue Excel-Datei wird am gleichen Ort gespeichert mit den gescrapten/erweiterten Daten und Columns.
