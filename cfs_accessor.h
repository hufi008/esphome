#include "esphome.h"
#include <vector>
#include <cstring>

class CFSRfidUtil {
public:
  static bool read_cfs_block(esphome::i2c::I2CBus *bus, uint8_t *uid, uint8_t *target_buffer) {
    uint8_t cfs_key[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
    uint8_t block = 4;
    uint8_t addr = 0x24; 

    // SCHRITT 1: Tag wieder aufwecken (InListPassiveTarget für 1 Karte, Typ ISO14443A)
    // Das holt das Tag aus dem Ruhezustand zurück, in den ESPHome es geschickt hat
    std::vector<uint8_t> wake_frame = {
      0x00, 0x00, 0xFF, 0x04, 0xFC,
      0xD4, 0x4A, 0x01, 0x00, 
      0xE1, 0x00 // Prüfsumme + Postambel
    };
    bus->write(addr, wake_frame.data(), wake_frame.size());
    delay(15); 

    // Dummy Read, um die Antwort des Wake-Ups aus dem PN532-Puffer zu löschen
    uint8_t dummy_rx[32];
    bus->read(addr, dummy_rx, 32);

    // SCHRITT 2: Authentifizierungskommando an Block 4 senden
    std::vector<uint8_t> auth_frame = {
      0x00, 0x00, 0xFF, 0x0F, 0xF1, 
      0xD4, 0x40, 0x01, 0x60, block
    };
    for (int i = 0; i < 6; i++) auth_frame.push_back(cfs_key[i]);
    for (int i = 0; i < 4; i++) auth_frame.push_back(uid[i]);
    
    uint8_t sum = 0;
    for (size_t i = 5; i < auth_frame.size(); i++) sum += auth_frame[i];
    auth_frame.push_back((uint8_t)(~sum + 1));
    auth_frame.push_back(0x00);

    if (bus->write(addr, auth_frame.data(), auth_frame.size()) != esphome::i2c::ERROR_OK) {
      return false;
    }
    delay(15);

    uint8_t auth_rx[16];
    bus->read(addr, auth_rx, 16);
    // Wenn Byte 7 im I2C-Frame 0x00 ist, war die Authentifizierung erfolgreich
    if (auth_rx[7] != 0x00) {
      return false;
    }

    // SCHRITT 3: Lesebefehl für Block 4 abfeuern
    std::vector<uint8_t> read_frame = {
      0x00, 0x00, 0xFF, 0x05, 0xFB,
      0xD4, 0x40, 0x01, 0x30, block,
      0xBF, 0x00 
    };

    if (bus->write(addr, read_frame.data(), read_frame.size()) != esphome::i2c::ERROR_OK) {
      return false;
    }
    delay(20);

    uint8_t rx_buf[32];
    if (bus->read(addr, rx_buf, 32) != esphome::i2c::ERROR_OK) {
      return false;
    }

    // Die 16 Byte Nutzdaten liegen bei einem PN532-I2C-Leseframe ab Index 8
    std::memcpy(target_buffer, &rx_buf[8], 16);
    return true;
  }
};
