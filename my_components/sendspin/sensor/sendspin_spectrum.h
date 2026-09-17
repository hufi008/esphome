#pragma once

#include "esphome/core/component.h"
#include "../sendspin_hub.h"

#include <mutex>
#include <utility>
#include <vector>

namespace esphome {
namespace sendspin_ {

class SendspinSpectrum : public SendspinChild {
 public:
  void setup() override {
    this->parent_->add_spectrum_callback(
        [this](int64_t client_timestamp, const std::vector<uint16_t> &bins) {
          std::lock_guard<std::mutex> lock(this->mutex_);
          this->pending_bins_ = bins;
          this->pending_ = true;
        });
  }

  void loop() override {
    std::vector<uint16_t> bins;

    {
      std::lock_guard<std::mutex> lock(this->mutex_);
      if (!this->pending_)
        return;

      bins.swap(this->pending_bins_);
      this->pending_ = false;
    }

    this->spectrum_callback_.call(bins);
  }

  template<typename F>
  void add_on_spectrum_callback(F &&callback) {
    this->spectrum_callback_.add(std::forward<F>(callback));
  }

 protected:
  CallbackManager<void(const std::vector<uint16_t> &)> spectrum_callback_;

  // Hufi
  std::mutex mutex_;
  std::vector<uint16_t> pending_bins_;
  bool pending_{false};
  // ifuH
};

}  // namespace sendspin_
}  // namespace esphome