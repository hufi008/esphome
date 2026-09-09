#include "sendspin_text_sensor.h"

// Hufi
#if defined(USE_ESP32) && (defined(USE_SENDSPIN_METADATA) || defined(USE_SENDSPIN_COLOR)) && defined(USE_TEXT_SENSOR)
// ifuH
#include <sendspin/metadata_role.h>
// Hufi
#include <sendspin/color_role.h>

#include <cstdio>
// ifuH
#include <string>

namespace esphome::sendspin_ {

static const char *const TAG = "sendspin.text_sensor";

// Hufi
Color to_color(const std::string &value) {
  unsigned int r = 0;
  unsigned int g = 0;
  unsigned int b = 0;

  std::sscanf(value.c_str(), "#%02X%02X%02X", &r, &g, &b);

  return Color(r, g, b);
}
// ifuH

void SendspinTextSensor::dump_config() { LOG_TEXT_SENSOR("", "Sendspin", this); }

// A field is nullopt when the server has not provided it or has explicitly cleared it. Both mean there is nothing to
// show, so return the empty string and let the caller publish it; returning early would leave the previous track's
// value on display.
//
// The empty string is not the same as unknown. A text sensor reports unknown through the API's missing_state flag,
// which follows has_state(), and has_state() is only ever set, never cleared. Once a real value has been published,
// an empty state is the closest we can get. The numeric sensors publish NAN, which does read as unknown.
const char *SendspinTextSensor::extract_value_(const sendspin::ServerMetadataStateObject &metadata) const {
// Hufi
  switch (this->type_) {
// ifuH
    case SendspinTextTypes::TITLE:
      return metadata.title.has_value() ? metadata.title.value().c_str() : "";
    case SendspinTextTypes::ARTIST:
      return metadata.artist.has_value() ? metadata.artist.value().c_str() : "";
    case SendspinTextTypes::ALBUM:
      return metadata.album.has_value() ? metadata.album.value().c_str() : "";
    case SendspinTextTypes::ALBUM_ARTIST:
      return metadata.album_artist.has_value() ? metadata.album_artist.value().c_str() : "";
    default:
      return "";
  }
}

// Hufi
const char *SendspinTextSensor::extract_value_(const sendspin::ServerColorStateObject &color) const {
  const std::optional<sendspin::RgbColor> *value = nullptr;

  switch (this->type_) {
    case SendspinTextTypes::PRIMARY:
      value = &color.primary;
      break;
    case SendspinTextTypes::ACCENT:
      value = &color.accent;
      break;
    case SendspinTextTypes::BACKGROUND_DARK:
      value = &color.background_dark;
      break;
    case SendspinTextTypes::BACKGROUND_LIGHT:
      value = &color.background_light;
      break;
    case SendspinTextTypes::ON_DARK:
      value = &color.on_dark;
      break;
    case SendspinTextTypes::ON_LIGHT:
      value = &color.on_light;
      break;
    default:
      return "";
  }

  static char buffer[8];

  if (!value->has_value()) {
    return "";
  }

  // Hufi
  const auto &rgb = value->value();
  std::snprintf(buffer, sizeof(buffer), "#%02X%02X%02X", rgb[0], rgb[1], rgb[2]);
  // ifuH
  return buffer;
}
// ifuH

// THREAD CONTEXT: Main loop. The registered metadata callback also fires on the main loop
// (SendspinHub dispatches metadata from client_->loop()).
void SendspinTextSensor::setup() {
  // Hufi
  switch (this->type_) {
    case SendspinTextTypes::TITLE:
    case SendspinTextTypes::ARTIST:
    case SendspinTextTypes::ALBUM:
    case SendspinTextTypes::ALBUM_ARTIST:
      this->parent_->add_metadata_update_callback([this](const sendspin::ServerMetadataStateObject &metadata) {
        this->publish_if_changed_(this->extract_value_(metadata));
      });
      break;

    case SendspinTextTypes::PRIMARY:
    case SendspinTextTypes::ACCENT:
    case SendspinTextTypes::BACKGROUND_DARK:
    case SendspinTextTypes::BACKGROUND_LIGHT:
    case SendspinTextTypes::ON_DARK:
    case SendspinTextTypes::ON_LIGHT:
      this->parent_->add_color_update_callback([this](const sendspin::ServerColorStateObject &color) {
        this->publish_if_changed_(this->extract_value_(color));
      });

      this->parent_->add_color_clear_callback([this]() {
        this->publish_if_changed_("");
      });
      break;
  }
  // ifuH
}

// Dedup to avoid frontend churn; TextSensor::publish_state already dedups the string assign but still notifies.
void SendspinTextSensor::publish_if_changed_(const char *value) {
  // The state starts empty, so a field that is already cleared when the first update arrives is suppressed here: the
  // entity stays unknown rather than being dropped out of it for good by an empty publish. Later clears do publish the
  // empty string and fire on_value with it.
  if (this->get_raw_state() != value) {
    this->publish_state(value);
  }
}

}  // namespace esphome::sendspin_

#endif
