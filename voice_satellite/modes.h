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
