import numpy as np
import soundfile as sf

SR = 48000  # Sample rate

# ---------------------------------------------------------
# Helper: write FLAC
# ---------------------------------------------------------
def save_flac(name, wave):
    sf.write(name, wave.astype(np.float32), SR, format='FLAC')
    print("Generated:", name)

# ---------------------------------------------------------
# Base helpers
# ---------------------------------------------------------
def tone(freq, t):
    return np.sin(2 * np.pi * freq * t)

def exp_decay(t, k=10):
    return np.exp(-t * k)

def lin_decay(t):
    return np.linspace(1.0, 0.0, len(t))

# ---------------------------------------------------------
# 1) error.flac – Sci‑Fi Error Glitch
# ---------------------------------------------------------
def make_error():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    carrier = 600 + 200 * np.sin(2 * np.pi * 40 * t)
    wave = 0.5 * np.sin(2 * np.pi * carrier * t)

    wave += 0.2 * np.sign(np.sin(2 * np.pi * 1200 * t))
    wave *= lin_decay(t)

    save_flac("error.flac", wave)

# ---------------------------------------------------------
# 2) success.flac – Sci‑Fi Confirmation Chime
# ---------------------------------------------------------
def make_success():
    duration = 0.35
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    tone1 = tone(880, t)
    tone2 = tone(1760, t)
    shimmer = tone(7, t)

    wave = 0.4 * (tone1 * (1 + 0.2 * shimmer) + 0.3 * tone2)
    wave *= lin_decay(t)

    save_flac("success.flac", wave)

# ---------------------------------------------------------
# 3) turn_on.flac – Power‑Up Sweep
# ---------------------------------------------------------
def make_turn_on():
    duration = 0.22
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    freq = np.linspace(300, 1500, len(t))
    wave = 0.45 * np.sin(2 * np.pi * freq * t)
    wave += 0.1 * np.sin(2 * np.pi * (freq * 2) * t)

    save_flac("turn_on.flac", wave)

# ---------------------------------------------------------
# 4) turn_off.flac – Power‑Down Sweep
# ---------------------------------------------------------
def make_turn_off():
    duration = 0.22
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    freq = np.linspace(1500, 200, len(t))
    wave = 0.45 * np.sin(2 * np.pi * freq * t)
    wave *= lin_decay(t)

    save_flac("turn_off.flac", wave)

# ---------------------------------------------------------
# 5) thinking.flac – Sci‑Fi Data Processing Pulse
# ---------------------------------------------------------
def make_thinking():
    duration = 0.45
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = np.zeros_like(t)

    def tick(start, end, freq):
        mask = (t > start) & (t < end)
        wave[mask] = 0.3 * np.sin(2 * np.pi * freq * t[mask])

    tick(0.05, 0.08, 1200)
    tick(0.18, 0.21, 900)
    tick(0.30, 0.33, 1500)

    wave += 0.05 * tone(70, t)

    save_flac("thinking.flac", wave)

# ---------------------------------------------------------
# 6) boot.flac – Startup Sweep
# ---------------------------------------------------------
def make_boot():
    duration = 0.35
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    freq = np.linspace(200, 1800, len(t))
    wave = 0.4 * np.sin(2 * np.pi * freq * t)
    wave *= exp_decay(t, 3)

    save_flac("boot.flac", wave)

# ---------------------------------------------------------
# 7) wake.flac – Wake Tone
# ---------------------------------------------------------
def make_wake():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.4 * tone(1000, t) + 0.2 * tone(2000, t)
    wave *= lin_decay(t)

    save_flac("wake.flac", wave)

# ---------------------------------------------------------
# 8) notify.flac – Notification Ping
# ---------------------------------------------------------
def make_notify():
    duration = 0.18
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.5 * tone(1500, t)
    wave *= exp_decay(t, 12)

    save_flac("notify.flac", wave)

# ---------------------------------------------------------
# 9) pause.flac – Pause Click
# ---------------------------------------------------------
def make_pause():
    duration = 0.08
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.5 * tone(800, t) * exp_decay(t, 25)

    save_flac("pause.flac", wave)

# ---------------------------------------------------------
# 10) single_click.flac – kurzer UI‑Click
# ---------------------------------------------------------
def make_single_click():
    duration = 0.06
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.55 * tone(1200, t) * exp_decay(t, 30)
    save_flac("single_click.flac", wave)

# ---------------------------------------------------------
# 11) double_click.flac – zwei kurze UI‑Clicks
# ---------------------------------------------------------
def make_double_click():
    duration = 0.14
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = np.zeros_like(t)

    m1 = (t >= 0.00) & (t < 0.06)
    wave[m1] = 0.55 * tone(1200, t[m1]) * exp_decay(t[m1], 30)

    m2 = (t >= 0.08) & (t < 0.14)
    wave[m2] = 0.55 * tone(1200, t[m2]) * exp_decay(t[m2], 30)

    save_flac("double_click.flac", wave)

# ---------------------------------------------------------
# 12) long_click.flac – langer, tieferer Click
# ---------------------------------------------------------
def make_long_click():
    duration = 0.18
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(900, t) * exp_decay(t, 10)
    save_flac("long_click.flac", wave)

# ---------------------------------------------------------
# 13) va_wake.flac – sanfter Wake‑Tone
# ---------------------------------------------------------
def make_va_wake():
    duration = 0.28
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(900, t) + 0.25 * tone(1800, t)
    wave *= lin_decay(t)

    save_flac("va_wake.flac", wave)

# ---------------------------------------------------------
# 14) va_confirm.flac – kurzer Bestätigungs‑Chime
# ---------------------------------------------------------
def make_va_confirm():
    duration = 0.22
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.5 * tone(1500, t) + 0.2 * tone(3000, t)
    wave *= exp_decay(t, 15)

    save_flac("va_confirm.flac", wave)

# ---------------------------------------------------------
# 15) va_reject.flac – Ablehnungs‑Tone
# ---------------------------------------------------------
def make_va_reject():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(400, t)
    wave *= exp_decay(t, 8)

    save_flac("va_reject.flac", wave)

# ---------------------------------------------------------
# 16) va_processing.flac – Sci‑Fi Processing Loop
# ---------------------------------------------------------
def make_va_processing():
    duration = 0.55
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = np.zeros_like(t)

    # Puls 1
    m1 = (t >= 0.05) & (t < 0.12)
    wave[m1] = 0.3 * tone(1200, t[m1]) * exp_decay(t[m1], 20)

    # Puls 2
    m2 = (t >= 0.20) & (t < 0.27)
    wave[m2] = 0.3 * tone(900, t[m2]) * exp_decay(t[m2], 20)

    # Puls 3
    m3 = (t >= 0.35) & (t < 0.42)
    wave[m3] = 0.3 * tone(1500, t[m3]) * exp_decay(t[m3], 20)

    # Hintergrund
    wave += 0.05 * tone(60, t)

    save_flac("va_processing.flac", wave)

# ---------------------------------------------------------
# 17) va_end.flac – Abschluss‑Tone
# ---------------------------------------------------------
def make_va_end():
    duration = 0.20
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.4 * tone(1000, t)
    wave *= lin_decay(t)

    save_flac("va_end.flac", wave)

# ---------------------------------------------------------
# 18) va_error.flac – Voice‑Assistant‑Error
# ---------------------------------------------------------
def make_va_error():
    duration = 0.30
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    carrier = 500 + 300 * np.sin(2 * np.pi * 35 * t)
    wave = 0.5 * np.sin(2 * np.pi * carrier * t)
    wave += 0.2 * np.sign(np.sin(2 * np.pi * 1100 * t))
    wave *= lin_decay(t)

    save_flac("va_error.flac", wave)

# ---------------------------------------------------------
# 19) va_notify.flac – Voice‑Assistant‑Notification
# ---------------------------------------------------------
def make_va_notify():
    duration = 0.18
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.5 * tone(1600, t)
    wave *= exp_decay(t, 12)

    save_flac("va_notify.flac", wave)

# ---------------------------------------------------------
# 20) va_idle.flac – sehr leiser Idle‑Tone
# ---------------------------------------------------------
def make_va_idle():
    duration = 0.35
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.05 * tone(40, t)
    wave *= lin_decay(t)

    save_flac("va_idle.flac", wave)

# ---------------------------------------------------------
# 21) va_attention.flac – Aufmerksamkeitssignal
# ---------------------------------------------------------
def make_va_attention():
    duration = 0.30
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(1300, t) + 0.15 * tone(2600, t)
    wave *= exp_decay(t, 10)

    save_flac("va_attention.flac", wave)

# ---------------------------------------------------------
# 22) va_chime_up.flac – kurzer Aufwärts‑Chime
# ---------------------------------------------------------
def make_va_chime_up():
    duration = 0.20
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    freq = np.linspace(600, 1600, len(t))
    wave = 0.4 * np.sin(2 * np.pi * freq * t)

    save_flac("va_chime_up.flac", wave)

# ---------------------------------------------------------
# 23) va_chime_down.flac – kurzer Abwärts‑Chime
# ---------------------------------------------------------
def make_va_chime_down():
    duration = 0.20
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    freq = np.linspace(1600, 600, len(t))
    wave = 0.4 * np.sin(2 * np.pi * freq * t)

    save_flac("va_chime_down.flac", wave)

# ---------------------------------------------------------
# 24) va_voice_start.flac – Start der Spracherfassung
# ---------------------------------------------------------
def make_va_voice_start():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(1100, t)
    wave *= exp_decay(t, 12)

    save_flac("va_voice_start.flac", wave)

# ---------------------------------------------------------
# 25) va_voice_end.flac – Ende der Spracherfassung
# ---------------------------------------------------------
def make_va_voice_end():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(700, t)
    wave *= exp_decay(t, 12)

    save_flac("va_voice_end.flac", wave)

# ---------------------------------------------------------
# 26) api_connect.flac – API erfolgreich verbunden
# ---------------------------------------------------------
def make_api_connect():
    duration = 0.12
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.40 * tone(900, t) + 0.25 * tone(1100, t)
    wave *= exp_decay(t, 10)

    save_flac("api_connect.flac", wave)

# ---------------------------------------------------------
# 27) api_disconnect.flac – API getrennt
# ---------------------------------------------------------
def make_api_disconnect():
    duration = 0.18
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(300, t) + 0.25 * tone(180, t)
    wave *= exp_decay(t, 8)

    save_flac("api_disconnect.flac", wave)

# ---------------------------------------------------------
# 28) wifi_connect.flac – WLAN verbunden
# ---------------------------------------------------------
def make_wifi_connect():
    t1 = np.linspace(0, 0.10, int(SR * 0.10), endpoint=False)
    t2 = np.linspace(0, 0.10, int(SR * 0.10), endpoint=False)

    ping1 = 0.40 * tone(700, t1) * exp_decay(t1, 10)
    ping2 = 0.40 * tone(900, t2) * exp_decay(t2, 10)

    silence = np.zeros(int(SR * 0.05))

    wave = np.concatenate([ping1, silence, ping2])
    save_flac("wifi_connect.flac", wave)

# ---------------------------------------------------------
# 29) wifi_disconnect.flac – WLAN getrennt
# ---------------------------------------------------------
def make_wifi_disconnect():
    duration = 0.20
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.35 * tone(600, t) + 0.25 * tone(350, t)
    wave *= exp_decay(t, 9)

    save_flac("wifi_disconnect.flac", wave)


# ---------------------------------------------------------
# Run all
# ---------------------------------------------------------
if __name__ == "__main__":
    make_error()
    make_success()
    make_turn_on()
    make_turn_off()
    make_thinking()
    make_boot()
    make_wake()
    make_notify()
    make_pause()
    make_single_click()
    make_double_click()
    make_long_click()
    make_va_wake()
    make_va_confirm()
    make_va_reject()
    make_va_processing()
    make_va_end()
    make_va_error()
    make_va_notify()
    make_va_idle()
    make_va_attention()
    make_va_chime_up()
    make_va_chime_down()
    make_va_voice_start()
    make_va_voice_end()
    make_api_connect()
    make_api_disconnect()
    make_wifi_connect()
    make_wifi_disconnect()
