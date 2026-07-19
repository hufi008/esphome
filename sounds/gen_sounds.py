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
# error.flac – Sci‑Fi Error Glitch
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
# success.flac – Sci‑Fi Confirmation Chime
# ---------------------------------------------------------
def make_success():
    duration = 0.40
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    # Harmonischer Dur-Akkord (Arpeggio-Feeling durch Phasen)
    wave = 0.3 * tone(523.25, t)  # C5
    wave += 0.2 * tone(659.25, t) # E5
    wave += 0.2 * tone(783.99, t) # G5
    wave += 0.15 * tone(1046.50, t) # C6 (Brillanz)
    
    # Ringmodulation für den "magischen" Sci-Fi-Schimmer
    wave *= (1.0 + 0.3 * np.sin(2 * np.pi * 35 * t))
    wave *= exp_decay(t, 7)
    save_flac("success.flac", wave)

# ---------------------------------------------------------
# turn_on.flac – Power‑Up Sweep
# ---------------------------------------------------------
def make_turn_on():
    duration = 0.08
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    # Extrem schneller Frequenz-Sweep nach oben für sofortiges Feedback
    freq = np.linspace(400, 1800, len(t))
    wave = 0.5 * np.sin(2 * np.pi * freq * t) * lin_decay(t)
    
    save_flac("turn_on.flac", wave)


# ---------------------------------------------------------
# turn_off.flac – Power‑Down Sweep
# ---------------------------------------------------------
def make_turn_off():
    duration = 0.08
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    # Extrem schneller Frequenz-Sweep nach unten
    freq = np.linspace(1600, 300, len(t))
    wave = 0.5 * np.sin(2 * np.pi * freq * t) * lin_decay(t)
    
    save_flac("turn_off.flac", wave)

# ---------------------------------------------------------
# thinking.flac – Sci‑Fi Data Processing Pulse
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
# boot.flac – Startup Sweep
# ---------------------------------------------------------
def make_boot():
    duration = 1.8  # Schön lang für den "Epik"-Faktor
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    # Ein tiefer, grollender Bass-Sub-Sweeep, der nach oben zieht
    f_bass = np.linspace(40, 120, len(t))
    bass = 0.3 * np.sin(2 * np.pi * f_bass * t)
    
    # Ein funkelnder, ansteigender Oberton-Akkord
    f_lead = np.linspace(300, 900, len(t))
    lead = 0.25 * np.sin(2 * np.pi * f_lead * t) + 0.15 * np.sin(2 * np.pi * (f_lead * 1.5) * t)
    
    wave = bass + lead
    # Sanftes Einblenden am Anfang, langsames Ausblenden am Ende
    fade_in = np.clip(t / 0.3, 0.0, 1.0)
    wave *= fade_in * exp_decay(t, 2.0)
    
    save_flac("boot.flac", wave)

# ---------------------------------------------------------
# wake.flac – Wake Tone
# ---------------------------------------------------------
def make_wake():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.4 * tone(1000, t) + 0.2 * tone(2000, t)
    wave *= lin_decay(t)

    save_flac("wake.flac", wave)

# ---------------------------------------------------------
# notify.flac – Notification Ping
# ---------------------------------------------------------
def make_notify():
    # Zwei ultrakurze, versetzte High-Tech-Pings
    t1 = np.linspace(0, 0.08, int(SR * 0.08), endpoint=False)
    t2 = np.linspace(0, 0.12, int(SR * 0.12), endpoint=False)
    
    p1 = 0.4 * tone(1600, t1) * exp_decay(t1, 40)
    p2 = 0.5 * tone(2200, t2) * exp_decay(t2, 25)
    silence = np.zeros(int(SR * 0.03))
    
    wave = np.concatenate([p1, silence, p2])
    save_flac("notify.flac", wave)

# ---------------------------------------------------------
# pause.flac – Pause Click
# ---------------------------------------------------------
def make_pause():
    duration = 0.08
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.5 * tone(800, t) * exp_decay(t, 25)

    save_flac("pause.flac", wave)

# ---------------------------------------------------------
# single_click.flac – kurzer UI‑Click
# ---------------------------------------------------------
def make_single_click():
    duration = 0.04
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    # Frequenz-Pitch-Drop für knackigen "Impact"
    freq = np.linspace(2500, 800, len(t))
    wave = 0.6 * np.sin(2 * np.pi * freq * t) * exp_decay(t, 80)
    save_flac("single_click.flac", wave)

# ---------------------------------------------------------
# double_click.flac – zwei kurze UI‑Clicks
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
# long_click.flac – langer, tieferer Click
# ---------------------------------------------------------
def make_long_click():
    duration = 0.18
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)

    wave = 0.45 * tone(900, t) * exp_decay(t, 10)
    save_flac("long_click.flac", wave)


# ---------------------------------------------------------
# chime_up.flac – kurzer Aufwärts‑Chime
# ---------------------------------------------------------
def make_chime_up():
    duration = 1.2
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    # 4 Töne, die nacheinander (Arpeggio) einsetzen und stehen bleiben
    wave = np.zeros_like(t)
    freqs = [440.0, 554.37, 659.25, 880.0]  # A-Dur Akkord
    delays = [0.0, 0.1, 0.2, 0.3]
    
    for f, d in zip(freqs, delays):
        mask = t >= d
        t_tone = t[mask] - d
        wave[mask] += 0.2 * tone(f, t_tone) * exp_decay(t_tone, 3.5)
        
    save_flac("chime_up.flac", wave)

# ---------------------------------------------------------
# chime_down.flac – kurzer Abwärts‑Chime
# ---------------------------------------------------------
def make_chime_down():
    duration = 1.2
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    # Gleicher Akkord wie chime_up, aber die Töne setzen von hoch nach tief ein
    wave = np.zeros_like(t)
    freqs = [880.0, 659.25, 554.37, 440.0]
    delays = [0.0, 0.1, 0.2, 0.3]
    
    for f, d in zip(freqs, delays):
        mask = t >= d
        t_tone = t[mask] - d
        wave[mask] += 0.2 * tone(f, t_tone) * exp_decay(t_tone, 3.5)
        
    save_flac("chime_down.flac", wave)

# ---------------------------------------------------------
# api_connect.flac – API erfolgreich verbunden
# ---------------------------------------------------------
def make_api_connect():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    
    # Ein sauberer, zweistufiger "Zipp"-Sound nach oben
    freq = np.linspace(600, 1400, len(t))
    wave = 0.4 * np.sin(2 * np.pi * freq * t) * exp_decay(t, 8)
    
    save_flac("api_connect.flac", wave)

# ---------------------------------------------------------
# api_disconnect.flac – API getrennt
# ---------------------------------------------------------
def make_api_disconnect():
    duration = 0.25
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    freq = np.linspace(600, 1400, len(t))
    wave_connect = 0.4 * np.sin(2 * np.pi * freq * t) * exp_decay(t, 8)
    
    # Array umdrehen -> Perfektes Gegenstück
    wave = np.flip(wave_connect)
    
    save_flac("api_disconnect.flac", wave)

# ---------------------------------------------------------
# wifi_connect.flac – WLAN verbunden
# ---------------------------------------------------------
def make_wifi_connect():
    duration = 1.0
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    wave = np.zeros_like(t)
    
    # 3 harmonische Töne, die nacheinander einsetzen und verklingen
    freqs = [587.33, 739.99, 1174.66]  # D-Dur Akkord (D5, F#5, D6)
    delays = [0.0, 0.08, 0.16]         # Schnelle, fließende Abfolge
    
    for f, d in zip(freqs, delays):
        mask = t >= d
        t_tone = t[mask] - d
        wave[mask] += 0.25 * tone(f, t_tone) * exp_decay(t_tone, 4.5)
        
    save_flac("wifi_connect.flac", wave)

# ---------------------------------------------------------
# wifi_disconnect.flac – WLAN getrennt
# ---------------------------------------------------------
def make_wifi_disconnect():
    duration = 1.0
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    wave_connect = np.zeros_like(t)
    
    # Basis für die Connect-Welle generieren
    freqs = [587.33, 739.99, 1174.66]
    delays = [0.0, 0.08, 0.16]
    
    for f, d in zip(freqs, delays):
        mask = t >= d
        t_tone = t[mask] - d
        wave_connect[mask] += 0.25 * tone(f, t_tone) * exp_decay(t_tone, 4.5)
        
    # Für den Disconnect-Effekt die Welle mathematisch umdrehen
    wave = np.flip(wave_connect)
    save_flac("wifi_disconnect.flac", wave)

# ---------------------------------------------------------
# timer_alarm.flac – Aufmerksamkeitsstarker Sci-Fi-Alarm
# ---------------------------------------------------------
def make_timer_alarm():
    # 3 Pulse von je 0.15s + 0.05s Pause = 0.6s Gesamtzeit
    duration = 0.60
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    wave = np.zeros_like(t)
    
    # Schneller, aggressiver Doppel-Pulse (Sireneneffekt)
    def alarm_pulse(t_clip):
        # Grundton moduliert durch eine schnelle Frequenzrampe
        f = 1200 + 400 * np.sin(2 * np.pi * 15 * t_clip)
        return 0.4 * np.sin(2 * np.pi * f * t_clip) + 0.15 * np.sign(np.sin(2 * np.pi * 2400 * t_clip))

    # Drei Pulse zeitlich platzieren
    m1 = (t >= 0.00) & (t < 0.15)
    wave[m1] = alarm_pulse(t[m1]) * lin_decay(t[m1])
    
    m2 = (t >= 0.20) & (t < 0.35)
    wave[m2] = alarm_pulse(t[m2]) * lin_decay(t[m2])
    
    m3 = (t >= 0.40) & (t < 0.55)
    wave[m3] = alarm_pulse(t[m3]) * lin_decay(t[m3])

    save_flac("timer_alarm.flac", wave)

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
    make_chime_up()
    make_chime_down()
    make_api_connect()
    make_api_disconnect()
    make_wifi_connect()
    make_wifi_disconnect()
    make_timer_alarm()

