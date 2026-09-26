import numpy as np
import soundfile as sf

# ---------------------------------------------------------
# spectrum_test.wav – logarithmischer Sweep 20 Hz -> 20 kHz
# ---------------------------------------------------------
def make_spectrum_test():
    TEST_SR = 48000
    duration = 30.0

    t = np.linspace(0, duration, int(TEST_SR * duration), endpoint=False)

    start_freq = 20.0
    end_freq = 20000.0

    # Logarithmischer Sweep:
    # dadurch werden tiefe und hohe Frequenzen gleichmäßig nach Oktaven durchlaufen.
    k = np.log(end_freq / start_freq) / duration
    phase = 2 * np.pi * start_freq * (np.exp(k * t) - 1.0) / k

    wave = 0.7 * np.sin(phase)

    # Sanft ein- und ausblenden, damit nichts klickt.
    fade_time = 0.02
    fade_samples = int(TEST_SR * fade_time)

    fade_in = np.linspace(0.0, 1.0, fade_samples)
    fade_out = np.linspace(1.0, 0.0, fade_samples)

    wave[:fade_samples] *= fade_in
    wave[-fade_samples:] *= fade_out

    sf.write(
        "spectrum_test.wav",
        wave.astype(np.float32),
        TEST_SR,
        format="WAV",
        subtype="PCM_16",
    )

    print("Generated: spectrum_test.wav")


# Aufruf:
make_spectrum_test()
