#include "color_sensor.h"

namespace esphome {
namespace color_sensor_ {

void ColorSensor::publish_state(const Color &color) {
  this->state_ = color;
  this->state_callback_.call(this->state_);
}

}  // namespace color_sensor_
}  // namespace esphome