# Version 3.0 Manifest (Erweitert)
## Refaktor: UI, Workflows etc.
Die Architektur wird auf ein modulares Widget-System umgestellt, bei dem alle UI-Elemente, Workflows und Datenbankelemente flexibel über Python, JSON und SQL konfiguriert werden.

### Kernkomponenten & Basisklassen

#### Basis-Widget (MenuOption)
Diese Module werden oben links in einem Menü angezeigt.


#### Basis-Widget (Tile)
Jedes Modul muss von der Basisklasse `Tile` erben. Diese Klasse dient als `Dependency-Injection-Container` und stellt alle notwendigen Abhängigkeiten als Attribute von self zur Verfügung.
 (Zugriff in TileModul)

|Injektion|Zweck|Beispiel|
|---|---|---|
|self.CONSTANTS|Globale Konfigurationen und Daten.|self.CONSTANTS.ROOT|
|self.SCOPES|Alle whitelisted, gescopeten Funktionen zur Ausführung von Systembefehlen.|self.SCOPES.cmd_start(...)|
|Button, Label, etc.|Gekapselte UI-Elemente zur Widget-Erstellung.|Button(self, ...)|

#### Sicherheit & Scopes
AST-Validierung und Regeln
* Es dürfen nur whitelisted und eigens erstellte Funktionen sowie Klassen aufgerufen werden.
* Eine AST-Analyse prüft den Code vor der Ausführung. Nicht konformer Code wird abgebrochen.
* Keine Imports sind in den Modulen notwendig und zulässig.
#### 🔍 Scopes
|Bereich|Scope-Name|Whitelisted Funktion (im self.SCOPES Objekt)|Einschränkung|
|---|---|---|---|
|Datenverarbeitung|lesen|file_read|C:/Windows/... ist untersagt|
|Datenverarbeitung|schreiben|file_write|C:/Windows/... ist untersagt|
|Datenverarbeitung|überschreiben|file_overwrite|C:/Windows/... ist untersagt|
|Datenverarbeitung|löschen|file_delete|C:/Windows/... ist untersagt|
|Zugriff Datenbank|read-only|db_read|-|Zugriff Datenbankrw (read-write)|db_execute|-|
|Zugriff Datenbank|wipe-out (komplett)|db_wipeout|-|
|Konsolenzugriff|start|cmd_start|C:/Windows/... ist untersagt|
|Konsolenzugriff|copy|cmd_copy|C:/Windows/... ist untersagt
|Konsolenzugriff|taskkill|cmd_taskkill|C:/Windows/... ist untersagt
|Konsolenzugriff|attrib|cmd_attrib|C:/Windows/... ist untersagt
|Konsolenzugriff|FFMPEG|cmd_ffmpeg|-|
|Konsolenzugriff|SOX|cmd_sox|-|
|Admin|-|-|Erfordert erhöhte Rechte|

#### Aufbau von Modulen & Paketen
* Paket
    * modules (Python logic limited)
        * Modul 1, Modul 2, ...
    * gui (JSON format capulated)
        * UI Window 1, UI Window 2, ...
    * menu
    * themes
    * SQL Layouts
    * Pack Image
    * License
    * readme.txt
    
#### Das TileModul: Help (Code & Scope)
Dies ist der korrigierte Code für das Help-Modul, das die Dependency-Injection-Regeln des Frameworks erfüllt.

```python
# TileModul: Beispiel Help
class Help(Tile):
    def __init__(self, parent, CONSTANTS, SCOPES): 
        super().__init__(parent)
        
        self.CONSTANTS = CONSTANTS
        self.SCOPES = SCOPES

        self.HELPFILEPATH = f'{self.CONSTANTS.ROOT}help.html'
        
        welcome_update_message(f'Create Helppage')
        
        Button(self, text="Show Help", command=self.gen_html).pack(expand=True, fill=tk.BOTH)

    def gen_html(self, *_):
        # Ruft file_write (Datenverarbeitung: schreiben) auf
        self.SCOPES.file_write(self.HELPFILEPATH, self.CONSTANTS.HELP)
        
        # Ruft cmd_start (Konsolenzugriff: start) auf
        self.SCOPES.cmd_start(self.HELPFILEPATH)
```

Erforderlicher Modul-Scope (help.scope.json)
```json
[
    "file_write",
    "cmd_start"
]
```

Das UIModul (JSON-Layout für den Button)
```json
[
    {
        "text": "x_button",
        "type": "btn",
        "root": "self",
        "command": "self.gen_html"
    }
]
```

SQL Layout Format (Datenbank-Struktur)
```json
{
    "db_01": [
        {"name": "a", "type": "TEXT"}, 
        {"name": "b", "type": "INTEGER"}, 
        {"name": "c", "type": "DATETIME"}
    ]
}
```

## Entferne Audacity aus dem Workflow

Audacity wird ersetzt mit SOX.

Es ist handlicher, verursacht weniger Probleme und vor allem es ist autmatisierbar.
Oben drauf kommt die User Experience.
Das installieren von Audacity & A-FFMPEG ist pain in the ass!
Mehr info #383

## MenuBar

LPRT bekommt nun auch eine MenuBar mit dieser lassen sich aktionen weiter optimieren.

Die standard optionen sind:
* LPRT
    * Lade Paket
    * License
    * Readme
    * Updates
    * Version
    * Schließen
* Language
    * English
    * German


## Gemini Integration wird entfernt

Da die Gemini integration nur wegen der Voraussetzungen der Masterschool existiert,
wird dies nun restlos entfernt!

Ob eine reintegration später notwendig sein wird, ist aktuell nicht bekannt.

Der Gemini code wird erstmal in `bin.removal` gespeichert.

## Refactoring der Dateien im Projekt

Aktuell sind Dateien so gespeichert: `bin.ui.file`

Es wird am Ende: `src.file`

> [!NOTE]
> Da der komplette hardcoded UI & Workflow Code entfernt wird werden auch keine Subfolder mehr notwendig sein!

