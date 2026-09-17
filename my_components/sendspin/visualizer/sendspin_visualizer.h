#pragma once

#include "esphome/core/component.h"
#include "../sendspin_hub.h"

#include <mutex>
#include <utility>
#include <vector>

namespace esphome {
namespace sendspin_ {

class SendspinVisualizer : public Component, public Parented<SendspinHub> {
 public:
  void setup() override;
  void loop() override;
  void dump_config() override;

  template<typename F> void add_on_spectrum_callback(F &&callback) {
    this->spectrum_callback_.add(std::forward<F>(callback));
  }

  template<typename F> void add_on_peak_callback(F &&callback) {
    this->peak_callback_.add(std::forward<F>(callback));
  }

  template<typename F> void add_on_beat_callback(F &&callback) {
    this->beat_callback_.add(std::forward<F>(callback));
  }

  template<typename F> void add_on_f_peak_callback(F &&callback) {
    this->f_peak_callback_.add(std::forward<F>(callback));
  }

  template<typename F> void add_on_loudness_callback(F &&callback) {
    this->loudness_callback_.add(std::forward<F>(callback));
  }

 protected:
  CallbackManager<void(const std::vector<uint16_t> &)> spectrum_callback_;
  CallbackManager<void(uint8_t)> peak_callback_;
  CallbackManager<void(bool)> beat_callback_;
  CallbackManager<void(uint16_t, uint16_t)> f_peak_callback_;
  CallbackManager<void(uint16_t)> loudness_callback_;

  std::mutex mutex_;
  std::optional<std::vector<uint16_t>> pending_spectrum_;
  std::optional<uint8_t> pending_peak_;
  std::optional<bool> pending_beat_;
  std::optional<std::pair<uint16_t, uint16_t>> pending_f_peak_;
  std::optional<uint16_t> pending_loudness_;
};


}  // namespace sendspin_
}  // namespace esphome