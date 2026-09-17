#pragma once

#include "esphome/core/component.h"
#include "esphome/core/color.h"
#include "esphome/components/color_sensor/color_sensor.h"
#include "../sendspin_hub.h"

#ifdef USE_SENDSPIN_COLOR
#include <sendspin/color_role.h>
#endif

namespace esphome {
namespace sendspin_ {

// Hufi
enum class SendspinColorTypes {
  PRIMARY,
  ACCENT,
  BACKGROUND_DARK,
  BACKGROUND_LIGHT,
  ON_DARK,
  ON_LIGHT,
};
// ifuH

class SendspinColorSensor : public color_sensor_::ColorSensor, public Parented<SendspinHub> {
 public:
  void setup() override;
  void dump_config() override;

  // Hufi
  void set_type(SendspinColorTypes type) { this->type_ = type; }

  void add_on_color_callback(std::function<void(const Color &)> &&callback) {
    this->color_callback_.add(std::move(callback));
  }

  void add_on_clear_callback(std::function<void()> &&callback) {
    this->clear_callback_.add(std::move(callback));
  }
  // ifuH

 protected:
  void publish_color_(const sendspin::ServerColorStateObject &color);

  // Hufi
  SendspinColorTypes type_{SendspinColorTypes::PRIMARY};
  CallbackManager<void(const Color &)> color_callback_;
  CallbackManager<void()> clear_callback_;
  // ifuH
};

}  // namespace sendspin_
}  // namespace esphome