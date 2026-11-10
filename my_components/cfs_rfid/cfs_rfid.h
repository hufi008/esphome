#pragma once

#include "esphome/core/component.h"
#include "esphome/components/i2c/i2c.h"
#include <vector>
#include <string>

namespace esphome {
namespace cfs_rfid {

class CFSRfidComponent : public PollingComponent, public i2c::I2CDevice {
 private:
  std::string last_uid_ = "";
  bool write_requested_ = false;
  std::string pending_write_text_ = "";

  bool send_pn532_cmd(const std::vector<uint8_t> &cmd, std::vector<uint8_t> &response, size_t reply_len);

 public:
  void setup() override;
  void update() override;
  void write_cfs_data(std::string text);
};

}  // namespace cfs_rfid
}  // namespace esphome
