#include "sendspin_color_sensor.h"

namespace esphome {
namespace sendspin_ {

// Hufi
void SendspinColorSensor::publish_color_(const sendspin::ServerColorStateObject &color) {
  const std::optional<sendspin::RgbColor> *value = nullptr;

  switch (this->type_) {
    case SendspinColorTypes::PRIMARY:
      value = &color.primary;
      break;
    case SendspinColorTypes::ACCENT:
      value = &color.accent;
      break;
    case SendspinColorTypes::BACKGROUND_DARK:
      value = &color.background_dark;
      break;
    case SendspinColorTypes::BACKGROUND_LIGHT:
      value = &color.background_light;
      break;
    case SendspinColorTypes::ON_DARK:
      value = &color.on_dark;
      break;
    case SendspinColorTypes::ON_LIGHT:
      value = &color.on_light;
      break;
  }

  if (!value->has_value()) {
    return;
  }

  const auto &rgb = value->value();
  Color color_state(rgb[0], rgb[1], rgb[2]);

  this->publish_state(color_state);
  this->color_callback_.call(color_state);
}
// ifuH

void SendspinColorSensor::setup() {
  // Hufi
  this->parent_->add_color_update_callback([this](const sendspin::ServerColorStateObject &color) {
    this->publish_color_(color);
  });

  this->parent_->add_color_clear_callback([this]() {
    this->clear_callback_.call();
  });
  // ifuH
}

void SendspinColorSensor::dump_config() {
  ESP_LOGCONFIG("sendspin_color_sensor", "Sendspin Color Sensor");
}

}  // namespace sendspin_
}  // namespace esphome