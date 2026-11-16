# Saurons Auge

ESPHome-Projekt für die animierte Augen-Darstellung und zusätzliche Uhranzeigen auf dem runden GC9A01-Display (240 × 240).

## Geräte-Konfigurationen

Die konkreten Geräte liegen im Verzeichnis `devices/`:

- `Saurons Eye c3.yaml` – ESP32-C3 SuperMini
- `Saurons Eye s3.yaml` – ESP32-S3 SuperMini

Die Geräte-YAMLs enthalten die Geräteidentität, Pinbelegung, die geräteabhängigen Animationsparameter und die eingebundenen Packages.

## Projektaufbau

- `hardware.yaml` – projektspezifische Entitäten, Uhrzeit, Fonts und Bedienung
- `main.yaml` – Display-Update und komplette Zeichen-/Animationslogik
- `../common/base-c3_supermini.yaml` bzw. `../common/base-s3_supermini.yaml` – Board-Grundlagen
- `../common/GC9A01.yaml` – SPI-Bus und Display-Initialisierung

Die Display-Initialisierung und Pinbelegung des GC9A01 bleiben im gemeinsamen Hardware-Baustein bzw. in der jeweiligen Geräte-YAML.

## Kompilieren

Vom Repository-Root aus:

```sh
esphome config "devices/Saurons Eye c3.yaml"
esphome compile "devices/Saurons Eye c3.yaml"

esphome config "devices/Saurons Eye s3.yaml"
esphome compile "devices/Saurons Eye s3.yaml"
```

Die ESPHome-Secrets müssen lokal vorhanden sein.
