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

<img width="400" height="300" alt="IMG_20260711_134434" src="https://github.com/user-attachments/assets/e1ee2a1c-2f93-4d2d-b0f1-97a8021d423f" />

---

## Architektur / Aufbau

### Zentrale Dateien
- speaker_2.yaml
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
- base-esp32.yaml
  - Standard-Settings API, WIFI
- my_components
  - Eigene ESPHome-C++-Komponenten für Media Player (Abfrage Buffer-Füllung)

### Hardware
  - esp32:
    - type: ESP32-S3 DevKitC 1
  - audio_output:
    - type: MAX98357A
    - pins:
      - spk_lrc_pin: GPIO40
      - spk_bclk_pin: GPIO39
      - spk_din_pin: GPIO38
    - notes:
      - spk_gain_pin:
        - 100kΩ GND = 15dB
        - GND = 12dB
        - offen = 9dB
        - VCC = 6dB
        - 100kΩ VCC = 3dB
      - spk_sd_pin:
        - offen = (L+R)/2
        - 370kΩ an VCC = rechts
        - 100kΩ an VCC = links
      - spk_gnd_pin: GND
      - spk_vin_pin: 5V
  - microphone:
    - type: INMP441
    - pins:
      - mic_ws_pin: GPIO06
      - mic_sck_pin: GPIO05
      - mic_sd_pin: GPIO04
    - notes:
      - mic_vdd_pin: 3V3
      - mic_gnd_pin: GND
      - mic_l_r_pin:
        - GND = links
        - VCC = rechts
  - leds:
    - type: WS2812
    - led_din_pin: GPIO42
    - count: 10
    - notes:
      - power: 5V
      - data: Pegelwandler empfohlen oder 100Ω an 3.3V bei kurzem Strip
  - i2c:
    - sda: GPIO17
    - scl: GPIO18
    - notes:
      - i2c_vin_pin: 3V3
      - i2c_gnd_pin: GND
      - notes:
        - Versorgung prüfen, VCC/GND können bei manchen Modulen umgekehrt sein. Hier bestimmt der MBE280 die Reihenfolge, da er direkt aufs Breadboard kommt.
  - oled_display:
    - type: SSD1306_128X64
    - address: 0x3C
  - buttons:
    - type: TTP221
    - pins:
      - btn_1_pin: GPIO11
      - btn_2_pin: GPIO12
      - btn_3_pin: GPIO13
      - btn_4_pin: GPIO14
    - notes:
      - btn_vcc_pin: 3V3
      - btn_gnd_pin: GND
  - power:
    - type: USBC-Buchse mit 4 Adern
      - Rot:     VIN 5V
      - Schwarz: GND
      - Weiss:   GPIO19
      - Blau:    GPIO20

- 2x speakers:
  - spec:
    - impedance: 4-8Ω
    - power: 3W

- supplies:
  - 2x breadboard
  - jumper wires
  - Dupont Flachbandkabel
  - USB-C Buchse mit 4 Adern
  - Widerstände


<img width="541" height="369" alt="esp32_s3_devkitC_1_pinout" src="https://github.com/user-attachments/assets/6e073c12-6965-416c-b2e4-191851b23a0d" />
<img width="515" height="388" alt="max98357_pinout" src="https://github.com/user-attachments/assets/a4faa96f-89c7-41c6-b4e7-449cfc5d7b93" />
<img width="357" height="292" alt="bme280_pinout" src="https://github.com/user-attachments/assets/8106e02c-684e-43b5-84ad-23468f04f898" />
<img width="420" height="476" alt="ttp221_pinout" src="https://github.com/user-attachments/assets/d7c43053-6569-44b4-a498-38e4827b4a08" />
<img width="446" height="448" alt="inmp441_pinout" src="https://github.com/user-attachments/assets/91df01ef-aa71-4732-8044-1a5fb9335251" />


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
- Prüfe speaker_2.yaml auf korrekte `substitutions` und `media_player_entity_id`

### 3. Konfiguration anpassen
- Passe `device_name` / `friendly_name` in speaker_2.yaml an
- Falls andere Pins genutzt werden, ändere sie in hardware.yaml
- Bei Bedarf base-s3_devkitc_1.yaml für WLAN/API anpassen

### 4. Flashen
- Über ESPHome USB oder OTA flashen
- speaker_2.yaml ist die Hauptdatei für dieses Gerät
- Für andere Geräte gibt es ähnliche YAML-Dateien wie speaker_3.yaml, speaker_4.yaml (alte HW-Anordnung mit Brücken)

<img width="400" height="300" alt="IMG_20260721_221848" src="https://github.com/user-attachments/assets/5e19ba3a-5551-44dc-9a45-cb9ba24faf7b" />

<img width="400" height="300" alt="IMG_20260721_222603" src="https://github.com/user-attachments/assets/c9a26b2f-6104-4e9f-8793-624b62ede0f3" />


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
