#pragma once

#include "esphome/core/component.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/time/real_time_clock.h"
#include "esphome/components/sun/sun.h"

namespace esphome {
namespace my_sun {

enum SunType {
  SUN_TYPE_SUNRISE,
  SUN_TYPE_SUNSET
};

class MySunSensor : public text_sensor::TextSensor, public PollingComponent {
 public:
  void set_type(SunType type) { type_ = type; }
  void set_format(const std::string &format) { format_ = format; }
  void set_time(time::RealTimeClock *time) { time_ = time; }
  void set_sun(sun::Sun *sun) { sun_ = sun; }

  void update() override {
    if (this->time_ == nullptr || !this->time_->now().is_valid() || this->sun_ == nullptr) {
      this->publish_state("--:--");
      return;
    }

    // Holt das aktuelle Datum/Uhrzeit vom ESP
    auto now_time = this->time_->now();

    // Greift auf die interne Positionsberechnung der offiziellen Sun-Komponente zu
    // Berechnet die Zeitpunkte bezogen auf den aktuellen Tag
    double sunrise_offset = this->sun_->get_location().sunrise_sunset_elevation(0.0, now_time, true);
    double sunset_offset = this->sun_->get_location().sunrise_sunset_elevation(0.0, now_time, false);

    // Fallback falls Berechnung fehlschlägt
    if (std::isnan(sunrise_offset) || std::isnan(sunset_offset)) {
      this->publish_state("--:--");
      return;
    }

    // Berechne den finalen Unix-Zeitstempel (Offset ist in Minuten ab Mitternacht UTC)
    // Wir nehmen den heutigen Tag (00:00 Uhr) und addieren das berechnete Offset
    ESPTime midnight = now_time;
    midnight.hour = 0;
    midnight.minute = 0;
    midnight.second = 0;
    
    time_t target_epoch = midnight.timestamp + (time_t)((type_ == SUN_TYPE_SUNRISE ? sunrise_offset : sunset_offset) * 60.0);

    // Echter ESPHome-Weg: Erstellt ein lokales Zeit-Objekt aus dem Unix-Zeitstempel
    ESPTime local_time = ESPTime::from_epoch_local(target_epoch);

    // Puffer befüllen und formatieren
    char buffer[32];
    size_t edge = local_time.strftime(buffer, sizeof(buffer), format_.c_str());
    
    if (edge > 0) {
      this->publish_state(std::string(buffer));
    } else {
      this->publish_state("--:--");
    }
  }

 protected:
  SunType type_;
  std::string format_;
  time::RealTimeClock *time_{nullptr};
  sun::Sun *sun_{nullptr};
};

}  // namespace my_sun
}  // namespace esphome
