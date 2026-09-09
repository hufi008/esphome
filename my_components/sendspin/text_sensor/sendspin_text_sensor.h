#pragma once

#include "esphome/core/defines.h"

// Hufi
#if defined(USE_ESP32) && (defined(USE_SENDSPIN_METADATA) || defined(USE_SENDSPIN_COLOR)) && defined(USE_TEXT_SENSOR)
// ifuH

#include "esphome/components/sendspin/sendspin_hub.h"
#include "esphome/components/text_sensor/text_sensor.h"

#include <sendspin/metadata_role.h>
// Hufi
#include <sendspin/color_role.h>
// ifuH

// Hufi
#include "esphome/core/color.h"
#include <string>
// ifuH

namespace esphome::sendspin_ {

// Hufi
  Color to_color(const std::string &value);
// ifuH

  // Hufi
enum class SendspinTextTypes {
  TITLE,
  ARTIST,
  ALBUM,
  ALBUM_ARTIST,
  PRIMARY,
  ACCENT,
  BACKGROUND_DARK,
  BACKGROUND_LIGHT,
  ON_DARK,
  ON_LIGHT,
};
// ifuH

// Hufi
class SendspinTextSensor final : public SendspinChild,
                                 public text_sensor::TextSensor,
                                 public sendspin::ColorRoleListener {
// ifuH
public:
  void dump_config() override;
  void setup() override;

// Hufi
  void set_type(SendspinTextTypes type) { this->type_ = type; }
// ifuH
 protected:
  const char *extract_value_(const sendspin::ServerMetadataStateObject &metadata) const;
// Hufi
  const char *extract_value_(const sendspin::ServerColorStateObject &color) const;
// ifuH
  void publish_if_changed_(const char *value);

// Hufi
SendspinTextTypes type_;
// ifuH
};

}  // namespace esphome::sendspin_
#endif
