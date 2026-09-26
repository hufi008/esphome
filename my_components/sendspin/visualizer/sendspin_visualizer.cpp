#include "sendspin_visualizer.h"

namespace esphome {
namespace sendspin_ {

void SendspinVisualizer::setup() {
  this->parent_->add_spectrum_callback(
      [this](int64_t client_timestamp, const std::vector<uint16_t> &bins) {
        std::lock_guard<std::mutex> lock(this->mutex_);
        this->pending_spectrum_ = bins;
      });

  this->parent_->add_peak_callback(
      [this](int64_t client_timestamp, uint8_t strength) {
        std::lock_guard<std::mutex> lock(this->mutex_);
        this->pending_peak_ = strength;
      });
  this->parent_->add_beat_callback(
      [this](int64_t client_timestamp, bool downbeat) {
        std::lock_guard<std::mutex> lock(this->mutex_);
        this->pending_beat_ = downbeat;
      });
  this->parent_->add_f_peak_callback(
    [this](int64_t client_timestamp,
           uint16_t frequency_hz,
           uint16_t amplitude) {
      std::lock_guard<std::mutex> lock(this->mutex_);
      this->pending_f_peak_ = {frequency_hz, amplitude};
    });
  this->parent_->add_loudness_callback(
      [this](int64_t client_timestamp, uint16_t loudness) {
        std::lock_guard<std::mutex> lock(this->mutex_);
        this->pending_loudness_ = loudness;
      });
}

void SendspinVisualizer::loop() {
  std::optional<std::vector<uint16_t>> spectrum;
  std::optional<uint8_t> peak;
  std::optional<bool> beat;
  std::optional<std::pair<uint16_t, uint16_t>> f_peak;
  std::optional<uint16_t> loudness;

  {
    std::lock_guard<std::mutex> lock(this->mutex_);

    spectrum = std::move(this->pending_spectrum_);
    peak = this->pending_peak_;
    beat = this->pending_beat_;
    f_peak = this->pending_f_peak_;
    loudness = this->pending_loudness_;

    this->pending_spectrum_.reset();
    this->pending_peak_.reset();
    this->pending_beat_.reset();
    this->pending_f_peak_.reset();
    this->pending_loudness_.reset();
  }

  if (spectrum.has_value())
    this->spectrum_callback_.call(*spectrum);

  if (peak.has_value())
    this->peak_callback_.call(*peak);

  if (beat.has_value())
    this->beat_callback_.call(*beat);

  if (f_peak.has_value())
    this->f_peak_callback_.call(f_peak->first, f_peak->second);

  if (loudness.has_value()) 
    this->loudness_callback_.call(*loudness);
}

void SendspinVisualizer::dump_config() {
  ESP_LOGCONFIG("sendspin_visualizer", "Sendspin Visualizer");

  const auto &config = this->parent_->get_visualizer_config();
  const auto &support = config.support;

  constexpr const char *type_names[] = {
      "BEAT",
      "LOUDNESS",
      "F_PEAK",
      "SPECTRUM",
      "PEAK",
  };

  std::string types = "[";
  for (size_t i = 0; i < support.types.size(); i++) {
    if (i > 0)
      types += ", ";
    types += type_names[static_cast<uint8_t>(support.types[i])];
  }
  types += "]";

  ESP_LOGCONFIG("sendspin.visualizer", "  Data types: %s", types.c_str());
  ESP_LOGCONFIG("sendspin.visualizer", "  Rate max: %u Hz", support.rate_max);
  ESP_LOGCONFIG("sendspin.visualizer", "  Buffer capacity: %u bytes", static_cast<unsigned>(support.buffer_capacity));
  ESP_LOGCONFIG("sendspin.visualizer", "  PSRAM stack: %s", config.psram_stack ? "YES" : "NO");
  ESP_LOGCONFIG("sendspin.visualizer", "  Priority: %u", config.priority);

  if (support.spectrum.has_value()) {
    const auto &spectrum = *support.spectrum;

    const char *scale = "UNKNOWN";
    switch (spectrum.scale) {
      case sendspin::VisualizerSpectrumScale::MEL:
        scale = "MEL";
        break;
      case sendspin::VisualizerSpectrumScale::LOG:
        scale = "LOG";
        break;
      case sendspin::VisualizerSpectrumScale::LIN:
        scale = "LIN";
        break;
    }

    ESP_LOGCONFIG("sendspin.visualizer", "  Spectrum bins: %u", spectrum.n_disp_bins);
    ESP_LOGCONFIG("sendspin.visualizer", "  Spectrum scale: %s", scale);
    ESP_LOGCONFIG("sendspin.visualizer", "  Spectrum range: %u - %u Hz", spectrum.f_min, spectrum.f_max);
  }
}

}  // namespace sendspin_
}  // namespace esphome