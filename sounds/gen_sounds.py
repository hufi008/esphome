import numpy as np
from scipy.io.wavfile import write

sr = 48000

def save(name, wave):
    write(name, sr, wave.astype(np.float32))
    print("Generated:", name)

# Stereo helper (dual mono)
def stereo(wave):
    return np.column_stack((wave, wave))

# ---------------------------------------------------------
# boot.wav – Rising Synth Startup
# ---------------------------------------------------------
def make_boot():
    duration = 0.9
    t = np.linspace(0, duration, int(sr*duration))

    freq = np.linspace(220, 880, len(t))
    wave = 0.4 * np.sin(2*np.pi*freq*t)

    chorus = 0.1 * np.sin(2*np.pi*(freq*0.97)*t)
    wave += chorus

    fade = np.linspace(0, 1, int(sr*0.1))
    wave[:len(fade)] *= fade
    wave[-len(fade):] *= fade[::-1]

    save("boot.wav", stereo(wave))

# ---------------------------------------------------------
# wake.wav – Sonar Ping
# ---------------------------------------------------------
def make_wake():
    duration = 0.18
    t = np.linspace(0, duration, int(sr*duration))

    freq = np.linspace(1600, 800, len(t))
    wave = 0.5 * np.sin(2*np.pi*freq*t)

    echo = np.zeros_like(wave)
    delay = int(0.04 * sr)
    echo[delay:] = 0.2 * wave[:-delay]
    wave += echo

    save("wake.wav", stereo(wave))

# ---------------------------------------------------------
# thinking.wav – Sci‑Fi Data Processing
# ---------------------------------------------------------
def make_thinking():
    duration = 0.45
    t = np.linspace(0, duration, int(sr*duration))

    wave = np.zeros_like(t)

    def tick(start, end, freq):
        mask = (t > start) & (t < end)
        wave[mask] = 0.3 * np.sin(2*np.pi*freq*t[mask])

    tick(0.05, 0.08, 1200)
    tick(0.18, 0.21, 900)
    tick(0.30, 0.33, 1500)

    wave += 0.05 * np.sin(2*np.pi*70*t)

    save("thinking.wav", stereo(wave))

# ---------------------------------------------------------
# notify.wav – Hologram Chime
# ---------------------------------------------------------
def make_notify():
    duration = 0.35
    t = np.linspace(0, duration, int(sr*duration))

    tone1 = np.sin(2*np.pi*880*t)
    tone2 = np.sin(2*np.pi*1760*t)
    shimmer = np.sin(2*np.pi*7*t)

    wave = 0.4 * (tone1*(1+0.2*shimmer) + 0.3*tone2)
    wave *= np.linspace(1, 0, len(t))

    save("notify.wav", stereo(wave))

# ---------------------------------------------------------
# pause.wav – Energy Click
# ---------------------------------------------------------
def make_pause():
    duration = 0.12
    t = np.linspace(0, duration, int(sr*duration))

    freq = np.linspace(200, 80, len(t))
    wave = 0.4 * np.sin(2*np.pi*freq*t)
    wave *= np.linspace(1, 0, len(t))

    save("pause.wav", stereo(wave))

# ---------------------------------------------------------
# error.wav – Sci‑Fi Error Glitch
# ---------------------------------------------------------
def make_error():
    duration = 0.25
    t = np.linspace(0, duration, int(sr*duration))

    carrier = 600 + 200*np.sin(2*np.pi*40*t)
    wave = 0.5 * np.sin(2*np.pi*carrier*t)

    wave += 0.2 * np.sign(np.sin(2*np.pi*1200*t))
    wave *= np.linspace(1, 0, len(t))

    save("error.wav", stereo(wave))

# ---------------------------------------------------------
# success.wav – Sci‑Fi Confirmation Chime
# ---------------------------------------------------------
def make_success():
    duration = 0.35
    t = np.linspace(0, duration, int(sr*duration))

    tone1 = np.sin(2*np.pi*880*t)
    tone2 = np.sin(2*np.pi*1760*t)
    shimmer = np.sin(2*np.pi*7*t)

    wave = 0.4 * (tone1*(1+0.2*shimmer) + 0.3*tone2)
    wave *= np.linspace(1, 0, len(t))

    save("success.wav", stereo(wave))

# ---------------------------------------------------------
# turn_on.wav – Power‑Up Sweep
# ---------------------------------------------------------
def make_turn_on():
    duration = 0.22
    t = np.linspace(0, duration, int(sr*duration))

    freq = np.linspace(300, 1500, len(t))
    wave = 0.45 * np.sin(2*np.pi*freq*t)
    wave += 0.1 * np.sin(2*np.pi*(freq*2)*t)

    save("turn_on.wav", stereo(wave))

# ---------------------------------------------------------
# turn_off.wav – Power‑Down Sweep
# ---------------------------------------------------------
def make_turn_off():
    duration = 0.22
    t = np.linspace(0, duration, int(sr*duration))

    freq = np.linspace(1500, 200, len(t))
    wave = 0.45 * np.sin(2*np.pi*freq*t)
    wave *= np.linspace(1, 0, len(t))

    save("turn_off.wav", stereo(wave))

# ---------------------------------------------------------
# red_alert.wav – Sci‑Fi Siren
# ---------------------------------------------------------
def make_red_alert():
    duration = 1.2
    t = np.linspace(0, duration, int(sr*duration))

    # 2-tone alternating siren
    tone1 = np.sin(2*np.pi*600*t)
    tone2 = np.sin(2*np.pi*900*t)

    # square-wave style switching
    switch = (np.sin(2*np.pi*2*t) > 0).astype(float)

    wave = 0.45 * (tone1 * switch + tone2 * (1 - switch))

    # slight distortion for aggression
    wave += 0.1 * np.sign(wave)

    save("red_alert.wav", stereo_fx(wave))
    
# ---------------------------------------------------------
# Generate all sounds
# ---------------------------------------------------------
make_boot()
make_wake()
make_thinking()
make_notify()
make_pause()
make_error()
make_success()
make_turn_on()
make_turn_off()
make_red_alert()
