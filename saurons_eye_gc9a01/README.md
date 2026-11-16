# Saurons Auge

ESPHome-Projekt für animierte Augen-Darstellung auf einem runden GC9A01-Display (240 × 240).

## Geräte-Konfigurationen

Die konkreten Geräte liegen im Verzeichnis `devices/`:

- `Saurons Eye c3.yaml` – ESP32-C3 SuperMini
- `Saurons Eye s3.yaml` – ESP32-S3 SuperMini
- `Saurons Eye s3 2.yaml` – weiteres ESP32-S3-Gerät

## Gemeinsame Bausteine

- `../common/base-c3_supermini.yaml` bzw. `../common/base-s3_supermini.yaml` – Board-Grundlagen
- `../common/GC9A01.yaml` – SPI-Bus und Display
- Die Animation und gerätespezifischen Einstellungen stehen in den jeweiligen Geräte-Konfigurationen.

## Kompilieren

Vom Repository-Root aus, zum Beispiel:

```sh
esphome config "devices/Saurons Eye s3.yaml"
esphome compile "devices/Saurons Eye s3.yaml"
```

Die ESPHome-Secrets müssen lokal vorhanden sein.
