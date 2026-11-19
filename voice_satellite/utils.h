#pragma once

#include <cmath>
#include <cstdint>
#include <functional>
#include <string>
#include <utility>
#include <vector>

namespace voice_satellite {

// Registriert einen Display-Seiten-Updater in der übergebenen Liste.
// ESPHome-Script-Aufrufe bleiben beim Aufrufer, damit ihre IDs im YAML-Kontext
// aufgelöst werden können.
inline void register_info_screen(std::vector<std::function<void()>> &screens,
                                 std::function<void()> updater) {
  screens.emplace_back(std::move(updater));
}

// Zeichnet einen zentrierten Text innerhalb eines begrenzten Bereichs.
// Überlange Texte laufen weich zwischen beiden Enden hin und her.
template<typename Display, typename Font, typename Alignment>
inline void scroll_marquee(Display &it, int center_x, int center_y, int text_width,
                           Font *font, const std::string &value,
                           Alignment alignment, uint32_t now_ms) {
  int tx, ty, tw, th;
  it.get_text_bounds(center_x, center_y, value.c_str(), font,
                     alignment, &tx, &ty, &tw, &th);

  const int text_half_width = tw / 2;
  const int area_half_width = text_width / 2;
  tx = center_x - area_half_width;
  tw = text_width;
  it.start_clipping(tx, ty, tx + tw, ty + th);

  if (text_half_width > area_half_width) {
    const float max_amplitude = text_half_width - area_half_width;
    constexpr float duration_move_ms = 3000.0f;
    constexpr float duration_pause_ms = 1200.0f;
    constexpr float total_cycle_ms = duration_move_ms * 2.0f + duration_pause_ms * 2.0f;
    const float current_time = std::fmod(static_cast<float>(now_ms), total_cycle_ms);
    float offset = 0.0f;

    if (current_time < duration_pause_ms) {
      offset = -max_amplitude;
    } else if (current_time < duration_pause_ms + duration_move_ms) {
      const float t = (current_time - duration_pause_ms) / duration_move_ms;
      const float smooth_t = t * t * (3.0f - 2.0f * t);
      offset = -max_amplitude + smooth_t * max_amplitude * 2.0f;
    } else if (current_time < duration_pause_ms * 2.0f + duration_move_ms) {
      offset = max_amplitude;
    } else {
      const float t = (current_time - duration_pause_ms * 2.0f - duration_move_ms) / duration_move_ms;
      const float smooth_t = t * t * (3.0f - 2.0f * t);
      offset = max_amplitude - smooth_t * max_amplitude * 2.0f;
    }

    it.print(center_x - offset, center_y, font, alignment, value.c_str());
  } else {
    it.print(center_x, center_y, font, alignment, value.c_str());
  }

  it.end_clipping();
}

}  // namespace voice_satellite
