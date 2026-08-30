#pragma once

#include "esphome/core/component.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/time/real_time_clock.h"
#include <string>

namespace esphome {
namespace my_moon {

const std::string MOON_KEYS[] = {
  "unknown",
  "new_moon", "waxing_crescent", "first_quarter", "waxing_gibbous",
  "full_moon", "waning_gibbous", "last_quarter", "waning_crescent"
};

class MoonSensor : public text_sensor::TextSensor, public PollingComponent {
 public:
  void set_time(time::RealTimeClock *time) { this->time_ = time; }

  void update() override {
    if (this->time_ == nullptr || !this->time_->now().is_valid()) {
      this->publish_state(MOON_KEYS[0]);
      return;
    }

    time_t now_ts = this->time_->now().timestamp;
    const time_t new_moon_ref = 947182440; 
    const double lunar_cycle = 2551442.87232;

    if (now_ts < new_moon_ref) {
      this->publish_state(MOON_KEYS[0]);
      return;
    }

    double diff_seconds = (double)(now_ts - new_moon_ref);
    double cycle_position = diff_seconds / lunar_cycle;
    cycle_position -= (long)cycle_position; 

    int phase_idx = 0;
    if (cycle_position < 0.03 || cycle_position >= 0.97) phase_idx = 1;
    else if (cycle_position >= 0.03 && cycle_position < 0.22) phase_idx = 2;
    else if (cycle_position >= 0.22 && cycle_position < 0.28) phase_idx = 3;
    else if (cycle_position >= 0.28 && cycle_position < 0.47) phase_idx = 4;
    else if (cycle_position >= 0.47 && cycle_position < 0.53) phase_idx = 5;
    else if (cycle_position >= 0.53 && cycle_position < 0.72) phase_idx = 6;
    else if (cycle_position >= 0.72 && cycle_position < 0.78) phase_idx = 7;
    else if (cycle_position >= 0.78 && cycle_position < 0.97) phase_idx = 8;

    this->publish_state(MOON_KEYS[phase_idx]);
  }

 protected:
  time::RealTimeClock *time_{nullptr};
};

}  // namespace my_moon
}  // namespace esphome
