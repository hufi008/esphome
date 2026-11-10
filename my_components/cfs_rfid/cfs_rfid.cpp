#include "cfs_rfid.h"
#include "esphome/core/log.h"
#include <cstring>

namespace esphome {
namespace cfs_rfid {

static const char *const TAG = "cfs_rfid";

void CFSRfidComponent::setup() {
  ESP_LOGI(TAG, "================================");
  ESP_LOGI(TAG, "PN532 Initialisierungstest");
  ESP_LOGI(TAG, "I2C-Adresse: 0x24");
  ESP_LOGI(TAG, "================================");

  // GetFirmwareVersion
  std::vector<uint8_t> cmd = {0x02};
  std::vector<uint8_t> reply;

  ESP_LOGI(TAG, "Sende GetFirmwareVersion...");

  if (!this->send_pn532_cmd(cmd, reply, 6)) {
    ESP_LOGE(TAG, "PN532 Firmwareabfrage fehlgeschlagen!");
    return;
  }

  ESP_LOGI(TAG, "Antwortlaenge: %u", reply.size());

  for (size_t i = 0; i < reply.size(); i++) {
    ESP_LOGI(TAG, "RX[%u] = 0x%02X", i, reply[i]);
  }

  ESP_LOGI(TAG, "Firmwareabfrage abgeschlossen.");
}

void CFSRfidComponent::update() {
  // InListPassiveTarget (Nach ISO14443A Tag suchen)
  std::vector<uint8_t> scan_cmd = {0x4A, 0x01, 0x00};
  std::vector<uint8_t> reply;
  
  if (!this->send_pn532_cmd(scan_cmd, reply, 20) || reply.size() < 12) {
    this->last_uid_ = "";
    return; // Keine Karte im Feld
  }

  // Anzahl gefundener Karten prüfen (Index 7 im Roh-Frame nach Header)
  if (reply[7] != 1) {
    this->last_uid_ = "";
    return;
  }

  // 4-Byte UID extrahieren (Mifare Classic, ab Index 12)
  uint8_t uid[4];
  std::memcpy(uid, &reply[12], 4);
  
  char uid_str[20];
  sprintf(uid_str, "%02X-%02X-%02X-%02X", uid[0], uid[1], uid[2], uid[3]);

  // Wenn ein Schreibbefehl aus HA ansteht, führen wir ihn jetzt aus
  if (this->write_requested_) {
    this->write_requested_ = false;
    ESP_LOGI(TAG, "Schreibvorgang gestartet fuer UID: %s", uid_str);

    // Authentifizierung an Block 4 mit Key A (0x60) und Default Key (6x 0xFF)
    std::vector<uint8_t> auth_cmd = {0x40, 0x01, 0x60, 4};
    for (int i = 0; i < 6; i++) auth_cmd.push_back(0xFF);
    for (int i = 0; i < 4; i++) auth_cmd.push_back(uid[i]);

    if (this->send_pn532_cmd(auth_cmd, reply, 10) && reply[7] == 0x00) {
      // Schreibpuffer füllen (16 Bytes, mit Leerzeichen auffüllen)
      std::vector<uint8_t> write_cmd = {0x40, 0x01, 0xA0, 4}; // 0xA0 = Mifare Write
      uint8_t write_buffer[16];
      std::memset(write_buffer, 0x20, 16);
      size_t len = std::min(this->pending_write_text_.length(), (size_t)16);
      std::memcpy(write_buffer, this->pending_write_text_.c_str(), len);
      for (int i = 0; i < 16; i++) write_cmd.push_back(write_buffer[i]);

      if (this->send_pn532_cmd(write_cmd, reply, 10) && reply[7] == 0x00) {
        ESP_LOGW(TAG, ">>> CFS TAG ERFOLGREICH BESCHRIEBEN!");
      } else {
        ESP_LOGE(TAG, "Schreibfehler auf Block 4.");
      }
    } else {
      ESP_LOGE(TAG, "Authentifizierung zum Schreiben fehlgeschlagen.");
    }
    return;
  }

  // Normaler Lesevorgang, falls das Tag neu im Feld ist
  if (this->last_uid_ != std::string(uid_str)) {
    this->last_uid_ = std::string(uid_str);
    ESP_LOGI(TAG, "Tag erkannt! UID: %s", uid_str);

    // Authentifizierung für Sektor 1 / Block 4
    std::vector<uint8_t> auth_cmd = {0x40, 0x01, 0x60, 4};
    for (int i = 0; i < 6; i++) auth_cmd.push_back(0xFF);
    for (int i = 0; i < 4; i++) auth_cmd.push_back(uid[i]);

    if (this->send_pn532_cmd(auth_cmd, reply, 10) && reply[7] == 0x00) {
      // Block 4 auslesen (0x30 = Mifare Read)
      std::vector<uint8_t> read_cmd = {0x40, 0x01, 0x30, 4};
      if (this->send_pn532_cmd(read_cmd, reply, 30) && reply[7] == 0x00 && reply.size() >= 24) {
        char ascii_str[17];
        std::memcpy(ascii_str, &reply[8], 16);
        ascii_str[16] = '\0';
        ESP_LOGW(TAG, ">>> CFS FILAMENT DATEN GELESEN: %s", ascii_str);
      } else {
        ESP_LOGE(TAG, "Fehler beim Lesen von Block 4.");
      }
    } else {
      ESP_LOGE(TAG, "Auth an Block 4 fehlgeschlagen (Falscher Key oder original verschluesselt).");
    }
  }
}

void CFSRfidComponent::write_cfs_data(std::string text) {
  this->pending_write_text_ = text;
  this->write_requested_ = true;
  ESP_LOGI(TAG, "Schreibwunsch registriert. Bitte Filament-Tag auflegen...");
}

bool CFSRfidComponent::send_pn532_cmd(const std::vector<uint8_t> &cmd, std::vector<uint8_t> &response, size_t reply_len) {
  std::vector<uint8_t> frame = {0x00, 0x00, 0xFF};
  uint8_t len = cmd.size() + 1; // +1 für 0xD4
  frame.push_back(len);
  frame.push_back((uint8_t)(~len + 1));
  frame.push_back(0xD4);
  for (uint8_t b : cmd) frame.push_back(b);
  
  uint8_t sum = 0xD4;
  for (uint8_t b : cmd) sum += b;
  frame.push_back((uint8_t)(~sum + 1));
  frame.push_back(0x00);

  // Nutzen der korrekten I2CDevice-Schreibmethode für rohe Payloads
  if (this->write(frame.data(), frame.size()) != i2c::ERROR_OK) return false;
  delay(10);

  // ACK (Bestaetigung, 7 Bytes) vom PN532 abholen
  uint8_t ack[7];
  if (this->read(ack, 7) != i2c::ERROR_OK) return false;
  ESP_LOGI(TAG, "PN532 ACK:");

  for (int i = 0; i < 7; i++) {
    ESP_LOGI(TAG, "ACK[%d] = 0x%02X", i, ack[i]);
  }

  if (ack[0] != 0x01) {
    ESP_LOGE(TAG, "PN532 nicht bereit! Status: 0x%02X", ack[0]);
    return false;
  }

  const uint8_t expected_ack[6] = {
    0x00, 0x00, 0xFF, 0x00, 0xFF, 0x00
  };

  if (memcmp(&ack[1], expected_ack, 6) != 0) {
    ESP_LOGE(TAG, "Ungueltiges PN532 ACK!");
    return false;
  }

  ESP_LOGI(TAG, "PN532 ACK erfolgreich!");

  if (reply_len == 0) return true;
  delay(10);

  // Antwort-Payload einlesen
  response.resize(reply_len + 7);
  if (this->read(response.data(), response.size()) != i2c::ERROR_OK) return false;
  
  return true;
}

}  // namespace cfs_rfid
}  // namespace esphome
