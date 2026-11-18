#pragma once

#include <cstdint>

// Zustände der untersten Darstellungsebene: Information und Media Player.
enum ContentMode : uint8_t {
  CONTENT_BOOT = 0,
  CONTENT_IDLE = 1,
  CONTENT_PLAY = 2,
  CONTENT_PAUSE = 3,
  CONTENT_SHUTDOWN = 4,
};

// Zustände der Assistant-Ebene.
enum AssistMode : uint8_t {
  ASSIST_IDLE = 0,
  ASSIST_LISTEN = 1,
  ASSIST_THINK = 2,
  ASSIST_ANNOUNCE = 3,
};

// Zustände der obersten Darstellungsebene.
enum OverlayMode : uint8_t {
  OVERLAY_NONE = 0,
  OVERLAY_VOLUME = 1,
  OVERLAY_ERROR = 2,
  OVERLAY_ALARM = 3,
};
