# Saurons Auge – ESP32-C3 SuperMini + GC9A01

Kleines ESPHome-Projekt für ein rundes 1,28"-GC9A01A-SPI-Display (240 × 240) am ESP32-C3 SuperMini.

## Aktueller Stand

Der eingecheckte Stand ist der nachweislich funktionierende Hallo-Welt-Test. Die Plasma-/Auge-Animation ist noch nicht enthalten.

## Dateien

- `supermini_1.yaml`: Hauptkonfiguration im Repository-Root
- `common/base-c3_supermini.yaml`: ESP32-C3-Basis
- `common/GC9A01.yaml`: SPI-Bus und GC9A01A-Display
- `common/base-esp32.yaml`: gemeinsame WLAN-, API- und OTA-Konfiguration

## Pinbelegung

| Display | ESP32-C3 SuperMini |
|---|---|
| GND | GND |
| VCC | 3V3 |
| SCL / SPI CLK | GPIO4 |
| SDA / SPI MOSI | GPIO3 |
| DC | GPIO2 |
| CS | GPIO1 |
| RST | GPIO0 |

## Voraussetzungen

Die ESPHome-Secrets müssen im ESPHome-Konfigurationsverzeichnis vorhanden sein. Benötigt werden die in `common/base-esp32.yaml` referenzierten Secrets für WLAN, API-Verschlüsselung, OTA und Fallback-AP.

## Kompilieren

Vom Repository-Root aus:

```sh
esphome config supermini_1.yaml
esphome compile supermini_1.yaml
```

## Display-Baseline

- Controller: GC9A01A
- Auflösung: 240 × 240
- SPI: 20 MHz, MODE0 (ESPHome-Standard)
- Farbinvertierung: aktiviert
- Rotation: 0°
- Aktualisierung: 1 Sekunde
