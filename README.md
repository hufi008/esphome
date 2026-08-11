# Home Assistant Voice Satellite
## Mein erstes ESP32 Projekt :-)

## Projektbeschreibung

Das ist ein ESPHome-basiertes Smart Speaker / Voice Assistant Satellite Projekt für ein `ESP32-S3`-basiertes Board.

### Was das Gerät kann
- Sprachsteuerung / Voice Assistant mit lokalem Wake Word
- I2S-Mikrofon `INMP441`
- I2S-Audioausgang via `MAX98357A` Verstärker
- LED-Statusring mit `WS2812`
- OLED-Display `SSD1306`
- Klima-/Wetterdaten über BME280 / HTU21
- Home Assistant Integration für Media Player, Text Sensoren, Sensoren, Button-Events
- Sounds und UI-Feedback (Boot, Wake, Fehler, Klicks, Timer etc.)
- Medien- und Ansage-Audioverwaltung

---

## Architektur / Aufbau

### Zentrale Dateien
- speaker_4.yaml
  - Hauptkonfiguration für das Gerät
  - Bezieht Basis-Setup, Hardware, Funktionen und Skripte per `packages`
- hardware.yaml
  - Pin-Definitionen
  - Sensor-/Aktuator-Konfiguration
  - Display, LEDs, I2S, Mikrofon, Speaker, Audio-Dateien
- main.yaml
  - Logik, Modi, Media Player Events, Voice Assistant Events
  - Content- / Overlay-Modi für Display & LEDs
  - API- und WLAN-Callbacks
- base-s3_devkitc_1.yaml
  - Basis-ESPHome-Setup für das verwendete Board
- my_components
  - Eigene ESPHome-C++-Komponenten für Media Player, Speaker, Sensoren, Textsensoren, Image-Handling

### Hardware
- ESP32-S3 Dev Kit C (oder ähnliches)
- I2S-Ausgang:
  - `GPIO11` LRC
  - `GPIO10` BCLK
  - `GPIO09` DIN
- I2S-Mikrofon:
  - `GPIO04` WS
  - `GPIO05` SCK
  - `GPIO06` SD
- LED-Streifen:
  - `GPIO08`
  - 10 LEDs
- I2C:
  - `GPIO01` SDA
  - `GPIO02` SCL
- Buttons:
  - `GPIO15`, `GPIO16`, `GPIO17`, `GPIO18`

---

## Wie du es nachbauen kannst

### 1. Hardware zusammenbauen
- Baue ESP32-S3 + MAX98357A + INMP441 + WS2812 + SSD1306 + Buttons
- Verbinde die Pins wie in hardware.yaml angegeben
- Optional: BME280 / HTU21 über I2C

### 2. Software vorbereiten
- Installiere ESPHome
- Lege das Projekt in esphome
- Stelle sicher, dass my_components und sounds im Projekt vorhanden sind
- Prüfe speaker_4.yaml auf korrekte `substitutions` und `media_player_entity_id`

### 3. Konfiguration anpassen
- Passe `device_name` / `friendly_name` in speaker_4.yaml an
- Falls andere Pins genutzt werden, ändere sie in hardware.yaml
- Bei Bedarf base-s3_devkitc_1.yaml für WLAN/API anpassen

### 4. Flashen
- Über ESPHome USB oder OTA flashen
- speaker_4.yaml ist die Hauptdatei für dieses Gerät
- Für andere Geräte gibt es ähnliche YAML-Dateien wie speaker_2.yaml, speaker_3.yaml, speaker_5.yaml

---

## Besonderheiten
- Das Projekt ist modular aufgebaut mit `packages:` und vielen `!extend`-Erweiterungen
- Es nutzt eigene ESPHome-Komponenten aus my_components
- Viele Zustände werden per globalen Variablen und Content-Modi gesteuert
- Die Medien- und Ansage-Funktion ist in `voice_assistant` und `media_player` eng verzahnt

---

## Empfehlung
Wenn du das nachbauen willst:
- Beginne mit einem einfachen Board + Display + LEDs
- Lass zuerst die Voice Assistant / Media Player-Integration weg
- Prüfe später Schritt für Schritt Mikrofon, Lautsprecher, Home Assistant
