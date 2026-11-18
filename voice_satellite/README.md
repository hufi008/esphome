# Voice Satellite

ESPHome-basiertes Smart-Speaker-/Voice-Assistant-Satellite-Projekt für ein ESP32-S3-Board.

## Projektstruktur

- `hardware.yaml` – zentrale Deklaration aller Hardware- und Infrastruktur-Komponenten, einschließlich LED-Strip, Zeit und WLAN-Sensorik
- `audio.yaml` – Audiofunktionen und Wiedergabe von UI-Sounds
- `assistant.yaml` – Home-Assistant Voice Assistant und Wake-Word-Ablauf
- `buttons.yaml` – Tastenfunktionen; GPIO-Binary-Sensoren werden aus `hardware.yaml` erweitert
- `display.yaml` – Displaydarstellung; trennt Statussymbole (`update_symbols`) und Displayinhalt (`update_content`), Display, Zeit und WLAN-Sensor werden aus `hardware.yaml` erweitert
- `ledstrip.yaml` – LED-Effekte und Prioritätsauflösung; die WS2812-Hardware wird aus `hardware.yaml` erweitert
- `modes.yaml` – typsichere Zustandsautomaten für Content, Assistant und Overlay; HA-Debug-Steuerung über Template-Selects
- `../my_components/` – eigene ESPHome-Komponenten
- `../sounds/` – Audio-Dateien

Die Hardware-Pins und die Geräteidentität werden in der jeweiligen Datei unter `devices/` festgelegt.

## Konfiguration prüfen und kompilieren

Vom Repository-Root aus:

```sh
esphome config devices/voice_satellite_1.yaml
esphome compile devices/voice_satellite_1.yaml
```

Die ESPHome-Secrets müssen lokal vorhanden sein. `secrets.yaml` wird nicht versioniert.
