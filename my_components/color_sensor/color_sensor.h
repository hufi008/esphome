#pragma once

#include "esphome/core/component.h"
#include "esphome/core/color.h"

namespace esphome {
namespace color_sensor_ {

class ColorSensor : public Component {
 public:
  void publish_state(const Color &color);

  template<typename F> void add_on_state_callback(F &&callback) {
    this->state_callback_.add(std::forward<F>(callback));
  }

  const Color &state() const { return this->state_; }

 protected:
  Color state_{};
  CallbackManager<void(const Color &)> state_callback_;
};

}  // namespace color_sensor_
}  // namespace esphome