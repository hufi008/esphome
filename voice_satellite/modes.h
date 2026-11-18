#pragma once

#include <cstdint>

// Zustände der untersten Darstellungsebene: Information und Media Player.
enum class ContentMode : uint8_t {
  BOOT = 0,
  IDLE = 1,
  PLAY = 2,
  PAUSE = 3,
  SHUTDOWN = 4,
};

// Zustände der Assistant-Ebene.
enum class AssistMode : uint8_t {
  IDLE = 0,
  LISTEN = 1,
  THINK = 2,
  ANNOUNCE = 3,
};

// Zustände der obersten Darstellungsebene.
enum class OverlayMode : uint8_t {
  NONE = 0,
  VOLUME = 1,
  ERROR = 2,
  ALARM = 3,
};

// Numeric HA debug controls are the only boundary between numbers and enums.
// All enum/integer conversions are kept here; the rest of the project stays typed.
#include <cmath>

template<typename Enum>
inline bool mode_from_number(float value, uint8_t max_value, Enum &mode) {
  if (!std::isfinite(value) || value < 0.0f || value > max_value ||
      std::floor(value) != value) {
    return false;
  }
  mode = static_cast<Enum>(static_cast<uint8_t>(value));
  return true;
}

template<typename Enum>
inline bool mode_to_number(Enum mode, uint8_t max_value, int &value) {
  const uint8_t raw = static_cast<uint8_t>(mode);
  if (raw > max_value) return false;
  value = static_cast<int>(raw);
  return true;
}

inline bool content_mode_from_number(float value, ContentMode &mode) {
  return mode_from_number(value, 4, mode);
}
inline bool assist_mode_from_number(float value, AssistMode &mode) {
  return mode_from_number(value, 3, mode);
}
inline bool overlay_mode_from_number(float value, OverlayMode &mode) {
  return mode_from_number(value, 3, mode);
}

inline bool content_mode_to_number(ContentMode mode, int &value) {
  return mode_to_number(mode, 4, value);
}
inline bool assist_mode_to_number(AssistMode mode, int &value) {
  return mode_to_number(mode, 3, value);
}
inline bool overlay_mode_to_number(OverlayMode mode, int &value) {
  return mode_to_number(mode, 3, value);
}
