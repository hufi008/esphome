# ESPHome-Projekte

Dieses Repository enthält mehrere ESPHome-Projekte, gemeinsam genutzte Konfigurationen und die dazugehörigen Geräte-Konfigurationen.

## Aufbau

| Verzeichnis | Inhalt |
|---|---|
| `devices/` | Konfigurationen der einzelnen physischen Geräte |
| `common/` | Gemeinsame Defaults, Board-Grundlagen und Hardware-Bausteine – keine Projektfunktionalität |
| `musicbox/` | MusicBox: Hardware-Definition und Funktionen |
| `akkubox/` | Akkubox: stromsparendes Sendspin-Projekt |
| `voice_satellite/` | Voice Satellite: Hardware, Funktionen und Skripte |
| `saurons_eye_gc9a01/` | Saurons Auge: Projektdokumentation |
| `my_components/` | Eigene ESPHome-Komponenten (Python/C++) |
| `sounds/` | Audiodateien für den Voice Satellite |
| `tests/` | Experimente und isolierte Test-Konfigurationen |

## Projekte

- **MusicBox** – Musikplayer mit Display, Touch, LEDs und Sendspin. Die AntBox-Geräte verwenden dieselbe MusicBox-Funktionalität und unterscheiden sich in der Hardware.
- **Akkubox** – eigenständiges, auf Akkubetrieb ausgelegtes Sendspin-Gerät mit monochromem Display und reduziertem Funktionsumfang.
- **Voice Satellite** – Sprachassistent mit Mikrofon, Lautsprecher, Status-LEDs und Audio-Feedback.
- **Saurons Auge** – animiertes Auge auf GC9A01-Displays.
- **RFID CFS Writer** – ESP32-Konfiguration zum Schreiben von CFS-Filament-Tags.

## Architektur

Eine Geräte-Konfiguration unter `devices/` beschreibt das konkrete Board und Gerät: Name, Substitutionswerte, Pins, verwendete Packages und gerätespezifische Abweichungen.

Die Projektverzeichnisse enthalten die jeweilige Hardware-Definition und die eigentliche Funktionalität. `common/` stellt wiederverwendbare Defaults und Hardware-Bausteine bereit, enthält aber bewusst keine Projektlogik. Eigene ESPHome-Komponenten liegen zentral in `my_components/`.

## Kompilieren

Die Konfigurationen werden vom Repository-Root aus aufgerufen. Beispiel:

```sh
esphome config devices/musicbox_2.yaml
esphome compile devices/musicbox_2.yaml
```

Vor einem ESPHome-Upgrade werden die Geräte-Konfigurationen zunächst mit der bisher verwendeten ESPHome-Version geprüft. Lokale `secrets.yaml`-Dateien gehören nicht ins Repository.
