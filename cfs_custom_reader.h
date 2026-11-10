#include "esphome.h"
#include <vector>
#include <cstring>

class CFSCustomReader : public Component {
 private:
  esphome::i2c::I2CBus *i2c_bus_;
  const uint8_t addr_ = 0x24; // Standard PN532 I2C-Adresse
  const uint8_t cfs_key_[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

 public:
  CFSCustomReader(esphome::i2c::I2CBus *bus) : i2c_bus_(bus) {}

  void setup() override {
    ESP_LOGI("cfs_custom", "Initialisiere PN532 über I2C...");
    
    // SAM Configuration Befehl (PN532 in normalen Modus versetzen)
    std::vector<uint8_t> sam_cmd = {0x00, 0x00, 0xFF, 0x05, 0xFB, 0xD4, 0x14, 0x01, 0x14, 0x00, 0x03, 0x00};
    i2c_bus_->write(addr_, sam_cmd.data(), sam_cmd.size());
    delay(10);
  }

  void loop() override {
    // 1. Suche nach ISO14443A Karte (InListPassiveTarget)
    std::vector<uint8_t> scan_cmd = {0x00, 0x00, 0xFF, 0x04, 0xFC, 0xD4, 0x4A, 0x01, 0x00, 0xE1, 0x00};
    if (i2c_bus_->write(addr_, scan_cmd.data(), scan_cmd.size()) != esphome::i2c::ERROR_OK) {
      return;
    }
    delay(15);

    uint8_t rx_buf[32] = {0};
    if (i2c_bus_->read(addr_, rx_buf, 32) != esphome::i2c::ERROR_OK) {
      return;
    }

    // Prüfen, ob eine Karte gefunden wurde (PN532 Antwort-Byte für gefundene Kartenanzahl an Index 7 muss > 0 sein)
    if (rx_buf[6] == 0x4B && rx_buf[7] == 0x01) {
      // UID extrahieren (befindet sich ab Index 12, Länge meist 4 Bytes bei Mifare Classic)
      uint8_t uid[4];
      std::memcpy(uid, &rx_buf[12], 4);
      
      ESP_LOGI("cfs_custom", "Tag erkannt! UID: %02X-%02X-%02X-%02X", uid[0], uid[1], uid[2], uid[3]);

      // 2. Authentifizierung an Sektor 1 (Block 4) mit Key A
      std::vector<uint8_t> auth_cmd = {0x00, 0x00, 0xFF, 0x0F, 0xF1, 0xD4, 0x40, 0x01, 0x60, 4};
      for (int i = 0; i < 6; i++) auth_cmd.push_back(cfs_key_[i]);
      for (int i = 0; i < 4; i++) auth_cmd.push_back(uid[i]);
      
      // Prüfsumme generieren
      uint8_t sum = 0;
      for (size_t i = 5; i < auth_cmd.size(); i++) sum += auth_cmd[i];
      auth_cmd.push_back((uint8_t)(~sum + 1));
      auth_cmd.push_back(0x00);

      i2c_bus_->write(addr_, auth_cmd.data(), auth_cmd.size());
      delay(15);
      
      uint8_t auth_resp[16] = {0};
      i2c_bus_->read(addr_, auth_resp, 16);

      // Bei Erfolg liefert die App-Schnittstelle im App-Status-Byte (Index 6) ein 0x00 zurück
      if (auth_resp[6] != 0x00) {
        ESP_LOGE("cfs_custom", "Authentifizierung für Block 4 fehlgeschlagen.");
        delay(2000); // Beruhigungszeit für das Log
        return;
      }

      // 3. Block 4 auslesen (Mifare Read = 0x30)
      std::vector<uint8_t> read_cmd = {0x00, 0x00, 0xFF, 0x05, 0xFB, 0xD4, 0x40, 0x01, 0x30, 4, 0xBF, 0x00};
      i2c_bus_->write(addr_, read_cmd.data(), read_cmd.size());
      delay(20);

      uint8_t data_resp[32] = {0};
      i2c_bus_->read(addr_, data_resp, 32);

      // Daten-Payload kopieren (liegt ab Index 8 im PN532 I2C-Datenframe)
      char ascii_str[17];
      std::memcpy(ascii_str, &data_resp[8], 16);
      ascii_str[16] = '\0'; // Terminierung

      ESP_LOGW("cfs_custom", ">>> GELESENE CFS DATEN: %s", ascii_str);
      
      delay(2500); // Pause, damit das Log bei aufgelegter Spule nicht flutet
    }
  }
};
