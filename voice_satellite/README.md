# Voice Satellite

ESPHome-basiertes Smart-Speaker-/Voice-Assistant-Satellite-Projekt für ein ESP32-S3-Board.

## Funktionen

- Sprachsteuerung / Voice Assistant mit lokalem Wake Word
- I2S-Mikrofon INMP441
- I2S-Audioausgang über MAX98357A
- WS2812-LED-Statusring
- OLED-Display
- Klima- und Wetterdaten (je nach Geräte-Konfiguration BME280 oder HTU21)
- Home-Assistant-Integration für Media Player, Textsensoren, Sensoren und Button-Events
- Audio-Feedback für Boot, Wake, Fehler, Klicks, Timer und weitere Ereignisse

## Projektstruktur

- `hardware.yaml` – Pins, Sensoren/Aktoren, Display, LEDs, I2S, Mikrofon, Lautsprecher und Audio-Dateien
- `main.yaml` – Voice-Assistant- und Media-Player-Logik, Modi, Events und Callbacks
- `scripts.yaml` – wiederverwendbare Skripte
- `../my_components/` – eigene ESPHome-Komponenten
- `../sounds/` – Audio-Dateien

Die physischen Geräte-Konfigurationen liegen unter `devices/`:
- `speaker_2.yaml`
- `speaker_3.yaml`
- `speaker_4.yaml`

## Hardware – Referenzaufbau

- ESP32-S3 DevKitC-1
- MAX98357A: BCLK GPIO39, LRC GPIO40, DIN GPIO38
- INMP441: WS GPIO6, SCK GPIO5, SD GPIO4
- WS2812: DIN GPIO42, 10 LEDs
- I²C: SDA GPIO17, SCL GPIO18
- OLED: SSD1306 128×64, Adresse 0x3C
- TTP221-Touch-Tasten: GPIO11 bis GPIO14

Die tatsächliche Pinbelegung und optionale Sensorbestückung ist je Gerät in der jeweiligen Datei unter `devices/` festgelegt.

## Kompilieren

Vom Repository-Root aus:

```sh
esphome config devices/speaker_2.yaml
esphome compile devices/speaker_2.yaml
```

Die ESPHome-Secrets müssen lokal vorhanden sein. `secrets.yaml` wird nicht versioniert.
