# Architecture Decision Record: Dokumentation

## Kontext
Die Dokumentation für das Projekt sollte einfach und flexibel gestaltet werden. Ziel ist es, eine leichtgewichtige Lösung zu finden, die Markdown-Dateien einfach zur verfügung stellt, ohne dass aufwändige Setups oder Pre-Compiler benötigt werden (wie bei z.B. mkdocs, pdocs oder sphinx). 

Die Dokumentation soll Wissen zu der Codebase ergänzen und für Anwender bereitstellen können, da dies ein Front-End eines Tools ist, wessen Zielgruppe Entwickler sind.

## Anforderungen:
- Schnelle Erstellung und Bearbeitung der Dokumentation.
- Nutzung von Markdown als primäres Format.
- Minimaler Overhead beim Deployment und Betrieb.
- Übersichtliche Ordnerstruktur mit Unterstützung für verschiedene Dokumentationsthemen.

## Entscheidung
Wir haben uns entschieden, eine selbstentwickelte Lösung zu verwenden. Diese Lösung basiert auf einer einfachen Ordnerstruktur und einer minimalen `metadata.yml`, die die Dokumentation in Sektionen strukturiert. Markdown-Dateien werden direkt gerendert, ohne dass ein Pre-Compiler oder komplizierte Tools erforderlich sind.

# Nutzung

## Relevante Klasse: `DocumentationCompiler`
Die Klasse `DocumentationCompiler` ist die zentrale Komponente, um Markdown-Dateien in HTML zu konvertieren und zu verwalten. Sie stellt zwei wichtige Methoden zur Verfügung:

- **Pfad:** `src/python/app/docs.py`

### Konstruktor

```python
def __init__(self, docs_folder, recompile=False):
```

#### Parameter: 
- **docs_folder**: Pfad zum Ordner, der die Markdown-Dateien enthält. 
- **recompile**: Wenn True, werden die HTML-Dateien bei jedem Aufruf von get_document neu generiert.

#### Beschreibung:
Der Konstruktor initialisiert die Instanz und legt fest, ob Dokumente bei jedem Abruf neu kompiliert werden sollen.

### Schnittstelle

```python
def get_document(self, filename)
```

#### Parameter:
- **filename**: Name der Markdown-Datei, die abgerufen werden soll.

#### Rückgabewert:
HTML-Content der entsprechenden Markdown-Datei.

#### Beschreibung:
Diese Methode liest die angeforderte Markdown-Datei und liefert deren HTML-Content zurück. Wenn recompile=True gesetzt ist, wird die HTML-Datei bei jedem Aufruf neu generiert.

## Ordnerstruktur
```plaintext
docs/
  metadata.yml        # Strukturierte Metadaten für die Navigation
  template.html       # Einfaches HTML-Template für die Darstellung
  index.md            # Hauptdokumentation oder Startseite
  adr/                # Architecture Decision Records
    docs.md           # Entscheidung zu Dokumentation
  stundenplan/        # Thematische Unterordner
    datamodel.md      # Dokument zu Datenmodellen
    pipeline.md       # Dokument zur Pipeline
  release/            # Versions- und Änderungsprotokoll
    r_0_0_1.md        # Release 0.0.1
    r_0_0_2.md        # Release 0.0.2
```

### metadata.yml
```
title: Stundenplan Dokumentation
sidebar:
  - header: Stundenplan
    topics:
      - name: Datenmodell
        file: stundenplan/datamodel.md
      - name: Pipeline
        file: stundenplan/pipeline.md
  - header: Implementation
    topics:
      - name: Server
        file: adr/server.md
```