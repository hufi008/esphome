import numpy as np
import soundfile as sf

# Optimierte Samplerate für den ESP32-S3 (Weniger RAM, native Pipeline-Frequenz)
SR = 16000  

# ---------------------------------------------------------
# Helper: schreibt unkomprimiertes WAV (PCM_16) statt FLAC
# ---------------------------------------------------------
def save_wav(name, wave):
    # Ändert das Dateiformat zu WAV und nutzt 16-Bit PCM
    sf.write(name, wave.astype(np.float32), SR, format='WAV', subtype='PCM_16')
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
# error.wav – Sci‑Fi Error Glitch
# ---------------------------------------------------------
def make_error():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    carrier = 600 + 200 * np.sin(2 * np.pi * 40 * t)
    wave = 0.5 * np.sin(2 * np.pi * carrier * t)

    wave += 0.2 * np.sign(np.sin(2 * np.pi * 1200 * t))
    wave *= lin_decay(t)

    save_wav("error.wav", wave)

# ---------------------------------------------------------
# success.wav – Sci‑Fi Confirmation Chime
# ---------------------------------------------------------
def make_success():
    duration = 0.40
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    wave = 0.3 * tone(523.25, t)  # C5
    wave += 0.2 * tone(659.25, t) # E5
    wave += 0.2 * tone(783.99, t) # G5
    wave += 0.15 * tone(1046.50, t) # C6
    
    wave *= (1.0 + 0.3 * np.sin(2 * np.pi * 35 * t))
    wave *= exp_decay(t, 7)
    save_wav("success.wav", wave)

# ---------------------------------------------------------
# turn_on.wav – Power‑Up Sweep
# ---------------------------------------------------------
def make_turn_on():
    duration = 0.08
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    freq = np.linspace(400, 1800, len(t))
    wave = 0.5 * np.sin(2 * np.pi * freq * t) * lin_decay(t)
    
    save_wav("turn_on.wav", wave)

# ---------------------------------------------------------
# turn_off.wav – Power‑Down Sweep
# ---------------------------------------------------------
def make_turn_off():
    duration = 0.08
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    freq = np.linspace(1600, 300, len(t))
    wave = 0.5 * np.sin(2 * np.pi * freq * t) * lin_decay(t)
    
    save_wav("turn_off.wav", wave)

# ---------------------------------------------------------
# thinking.wav – Sci‑Fi Data Processing Pulse
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

    save_wav("thinking.wav", wave)

# ---------------------------------------------------------
# boot.wav – Startup Sweep
# ---------------------------------------------------------
def make_boot():
    duration = 1.8  
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    f_bass = np.linspace(40, 120, len(t))
    bass = 0.3 * np.sin(2 * np.pi * f_bass * t)
    
    f_lead = np.linspace(300, 900, len(t))
    lead = 0.25 * np.sin(2 * np.pi * f_lead * t) + 0.15 * np.sin(2 * np.pi * (f_lead * 1.5) * t)
    
    wave = bass + lead
    fade_in = np.clip(t / 0.3, 0.0, 1.0)
    wave *= fade_in * exp_decay(t, 2.0)
    
    save_wav("boot.wav", wave)

# ---------------------------------------------------------
# wake.wav – Wake Tone
# ---------------------------------------------------------
def make_wake():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.4 * tone(1000, t) + 0.2 * tone(2000, t)
    wave *= lin_decay(t)

    save_wav("wake.wav", wave)

# ---------------------------------------------------------
# notify.wav – Notification Ping
# ---------------------------------------------------------
def make_notify():
    t1 = np.linspace(0, 0.08, int(SR * 0.08), endpoint=False)
    t2 = np.linspace(0, 0.12, int(SR * 0.12), endpoint=False)
    
    p1 = 0.4 * tone(1600, t1) * exp_decay(t1, 40)
    p2 = 0.5 * tone(2200, t2) * exp_decay(t2, 25)
    silence = np.zeros(int(SR * 0.03))
    
    wave = np.concatenate([p1, silence, p2])
    save_wav("notify.wav", wave)

# ---------------------------------------------------------
# pause.wav – Pause Click
# ---------------------------------------------------------
def make_pause():
    duration = 0.08
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.5 * tone(800, t) * exp_decay(t, 25)

    save_wav("pause.wav", wave)

# ---------------------------------------------------------
# single_click.wav – kurzer UI‑Click
# ---------------------------------------------------------
def make_single_click():
    duration = 0.04
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    freq = np.linspace(2500, 800, len(t))
    wave = 0.6 * np.sin(2 * np.pi * freq * t) * exp_decay(t, 80)
    save_wav("single_click.wav", wave)

# ---------------------------------------------------------
# double_click.wav – zwei kurze UI‑Clicks
# ---------------------------------------------------------
def make_double_click():
    duration = 0.14
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = np.zeros_like(t)

    m1 = (t >= 0.00) & (t < 0.06)
    wave[m1] = 0.55 * tone(1200, t[m1]) * exp_decay(t[m1], 30)

    m2 = (t >= 0.08) & (t < 0.14)
    wave[m2] = 0.55 * tone(1200, t[m2]) * exp_decay(t[m2], 30)

    save_wav("double_click.wav", wave)

# ---------------------------------------------------------
# long_click.wav – langer, tieferer Click
# ---------------------------------------------------------
def make_long_click():
    duration = 0.18
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(900, t) * exp_decay(t, 10)
    save_wav("long_click.wav", wave)

# ---------------------------------------------------------
# chime_up.wav – kurzer Aufwärts‑Chime
# ---------------------------------------------------------
def make_chime_up():
    duration = 1.2
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    wave = np.zeros_like(t)
    freqs = [440.0, 554.37, 659.25, 880.0]  
    delays = [0.0, 0.1, 0.2, 0.3]
    
    for f, d in zip(freqs, delays):
        mask = t >= d
        t_tone = t[mask] - d
        wave[mask] += 0.2 * tone(f, t_tone) * exp_decay(t_tone, 3.5)
        
    save_wav("chime_up.wav", wave)

# ---------------------------------------------------------
# chime_down.wav – kurzer Abwärts‑Chime
# ---------------------------------------------------------
def make_chime_down():
    duration = 1.2
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    wave = np.zeros_like(t)
    freqs = [880.0, 659.25, 554.37, 440.0]
    delays = [0.0, 0.1, 0.2, 0.3]
    
    for f, d in zip(freqs, delays):
        mask = t >= d
        t_tone = t[mask] - d
        wave[mask] += 0.2 * tone(f, t_tone) * exp_decay(t_tone, 3.5)
        
    save_wav("chime_down.wav", wave)

# ---------------------------------------------------------
# api_connect.wav – API erfolgreich verbunden
# ---------------------------------------------------------
def make_api_connect():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    freq = np.linspace(600, 1400, len(t))
    wave = 0.4 * np.sin(2 * np.pi * freq * t) * exp_decay(t, 8)
    
    save_wav("api_connect.wav", wave)

# ---------------------------------------------------------
# api_disconnect.wav – API getrennt
# ---------------------------------------------------------
def make_api_disconnect():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    freq = np.linspace(600, 1400, len(t))
    wave_connect = 0.4 * np.sin(2 * np.pi * freq * t) * exp_decay(t, 8)
    
    wave = np.flip(wave_connect)
    
    save_wav("api_disconnect.wav", wave)

# ---------------------------------------------------------
# wifi_connect.wav – WLAN verbunden
# ---------------------------------------------------------
def make_wifi_connect():
    duration = 1.0
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    wave = np.zeros_like(t)
    
    freqs = [587.33, 739.99, 1174.66]  
    delays = [0.0, 0.08, 0.16]         
    
    for f, d in zip(freqs, delays):
        mask = t >= d
        t_tone = t[mask] - d
        wave[mask] += 0.25 * tone(f, t_tone) * exp_decay(t_tone, 4.5)
        
    save_wav("wifi_connect.wav", wave)

# ---------------------------------------------------------
# wifi_disconnect.wav – WLAN getrennt
# ---------------------------------------------------------
def make_wifi_disconnect():
    duration = 1.0
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    wave_connect = np.zeros_like(t)
    
    freqs = [587.33, 739.99, 1174.66]
    delays = [0.0, 0.08, 0.16]
    
    for f, d in zip(freqs, delays):
        mask = t >= d
        t_tone = t[mask] - d
        wave_connect[mask] += 0.25 * tone(f, t_tone) * exp_decay(t_tone, 4.5)
        
    wave = np.flip(wave_connect)
    save_wav("wifi_disconnect.wav", wave)

# ---------------------------------------------------------
# timer_alarm.wav – Aufmerksamkeitsstarker Sci-Fi-Alarm
# ---------------------------------------------------------
def make_timer_alarm():
    duration = 0.60
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    wave = np.zeros_like(t)
    
    def alarm_pulse(t_clip):
        f = 1200 + 400 * np.sin(2 * np.pi * 15 * t_clip)
        return 0.4 * np.sin(2 * np.pi * f * t_clip) + 0.15 * np.sign(np.sin(2 * np.pi * 2400 * t_clip))

    m1 = (t >= 0.00) & (t < 0.15)
    wave[m1] = alarm_pulse(t[m1]) * lin_decay(t[m1])
    
    m2 = (t >= 0.20) & (t < 0.35)
    wave[m2] = alarm_pulse(t[m2]) * lin_decay(t[m2])
    
    m3 = (t >= 0.40) & (t < 0.55)
    wave[m3] = alarm_pulse(t[m3]) * lin_decay(t[m3])

    save_wav("timer_alarm.wav", wave)

# ---------------------------------------------------------
# Alle Generatoren ausführen (WAV-Gesamtübersicht)
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
    make_chime_up()
    make_chime_down()
    make_api_connect()
    make_api_disconnect()
    make_wifi_connect()
    make_wifi_disconnect()
    make_timer_alarm()
