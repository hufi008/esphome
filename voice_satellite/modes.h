#pragma once

#include <cstddef>
#include <cstdint>
#include <cstring>

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
  NONE = 0,
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

// Home-Assistant-Debug-Selects verwenden dieselben Namen wie die Enum-Werte.
// Die Zuordnung liegt zentral hier; im YAML gibt es keine Integer-Konvertierung.
template<typename Enum>
struct ModeOption {
  const char *name;
  Enum value;
};

template<typename Enum, size_t N>
inline bool mode_from_string(const char *name, const ModeOption<Enum> (&options)[N], Enum &mode) {
  if (name == nullptr) return false;
  for (const auto &option : options) {
    if (std::strcmp(name, option.name) == 0) {
      mode = option.value;
      return true;
    }
  }
  return false;
}

template<typename Enum, size_t N>
inline const char *mode_to_string(Enum mode, const ModeOption<Enum> (&options)[N]) {
  for (const auto &option : options) {
    if (mode == option.value) return option.name;
  }
  return nullptr;
}

inline constexpr ModeOption<ContentMode> CONTENT_MODE_OPTIONS[] = {
    {"BOOT", ContentMode::BOOT},
    {"IDLE", ContentMode::IDLE},
    {"PLAY", ContentMode::PLAY},
    {"PAUSE", ContentMode::PAUSE},
    {"SHUTDOWN", ContentMode::SHUTDOWN},
};

inline constexpr ModeOption<AssistMode> ASSIST_MODE_OPTIONS[] = {
    {"NONE", AssistMode::NONE},
    {"LISTEN", AssistMode::LISTEN},
    {"THINK", AssistMode::THINK},
    {"ANNOUNCE", AssistMode::ANNOUNCE},
};

inline constexpr ModeOption<OverlayMode> OVERLAY_MODE_OPTIONS[] = {
    {"NONE", OverlayMode::NONE},
    {"VOLUME", OverlayMode::VOLUME},
    {"ERROR", OverlayMode::ERROR},
    {"ALARM", OverlayMode::ALARM},
};

inline bool content_mode_from_string(const char *name, ContentMode &mode) {
  return mode_from_string(name, CONTENT_MODE_OPTIONS, mode);
}
inline const char *content_mode_to_string(ContentMode mode) {
  return mode_to_string(mode, CONTENT_MODE_OPTIONS);
}

inline bool assist_mode_from_string(const char *name, AssistMode &mode) {
  return mode_from_string(name, ASSIST_MODE_OPTIONS, mode);
}
inline const char *assist_mode_to_string(AssistMode mode) {
  return mode_to_string(mode, ASSIST_MODE_OPTIONS);
}

inline bool overlay_mode_from_string(const char *name, OverlayMode &mode) {
  return mode_from_string(name, OVERLAY_MODE_OPTIONS, mode);
}
inline const char *overlay_mode_to_string(OverlayMode mode) {
  return mode_to_string(mode, OVERLAY_MODE_OPTIONS);
}
