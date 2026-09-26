import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 44100
DURATION = 12.0
total_samples = int(SAMPLE_RATE * DURATION)
t = np.linspace(0, DURATION, total_samples, endpoint=False)

# 1. Ambient Sub-Bass Drone (Hans Zimmer style deep drone at 50Hz + 100Hz + 150Hz)
drone_freq = 55.0  # Low A
drone = 0.35 * np.sin(2 * np.pi * drone_freq * t) + \
        0.18 * np.sin(2 * np.pi * (drone_freq * 2) * t) + \
        0.08 * np.sin(2 * np.pi * (drone_freq * 3) * t)
# Add subtle low frequency pulse (LFO at 0.5 Hz)
lfo = 0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t)
drone = drone * lfo

# 2. Driving Tech Arpeggiator (120 BPM -> 1 beat = 0.5s, 16th notes = 0.125s)
arp = np.zeros(total_samples)
bpm = 120.0
step_len = int(SAMPLE_RATE * 60.0 / bpm / 2) # 8th notes (0.25s)
# Cyber chord progression: A minor -> F -> C -> G
notes = [
    220.0, 330.0, 440.0, 330.0,  # A min
    220.0, 330.0, 523.25, 330.0,
    174.6, 261.6, 349.2, 261.6,  # F maj
    196.0, 293.6, 392.0, 293.6   # G maj
]
note_idx = 0
for start in range(0, total_samples, step_len):
    end = min(start + step_len, total_samples)
    seg_len = end - start
    st = np.linspace(0, seg_len / SAMPLE_RATE, seg_len, endpoint=False)
    freq = notes[note_idx % len(notes)]
    # Pluck envelope
    env = np.exp(-st * 12.0)
    # Synth pluck (saw + sine)
    synth = 0.12 * (np.sin(2 * np.pi * freq * st) + 0.5 * np.sin(2 * np.pi * 2 * freq * st)) * env
    arp[start:end] += synth
    note_idx += 1

# 3. Transition Whooshes at t=3.6s and t=7.6s
whoosh = np.zeros(total_samples)
for wt in [3.6, 7.6]:
    w_start = int((wt - 0.4) * SAMPLE_RATE)
    w_end = int((wt + 0.6) * SAMPLE_RATE)
    w_len = w_end - w_start
    w_t = np.linspace(0, 1.0, w_len)
    noise = np.random.uniform(-1, 1, w_len)
    # Bandpass / envelope simulation
    env = np.sin(np.pi * w_t)**2
    pitch_sweep = np.sin(2 * np.pi * (150 + 800 * (w_t**2)) * w_t)
    whoosh[w_start:w_end] += 0.25 * env * (0.6 * noise + 0.4 * pitch_sweep)

# 4. Cinematic Braam / Hit at t=7.8s (Hero Halt & Stare)
braam = np.zeros(total_samples)
b_start = int(7.8 * SAMPLE_RATE)
b_len = int(3.5 * SAMPLE_RATE)
b_end = min(b_start + b_len, total_samples)
actual_len = b_end - b_start
bt = np.linspace(0, actual_len / SAMPLE_RATE, actual_len, endpoint=False)
# Heavy brass / reese bass hit (F# down to D)
b_freq = 48.0 * np.exp(-bt * 0.15)
b_env = np.exp(-bt * 1.2) * (1.0 - np.exp(-bt * 30.0)) # sharp attack, smooth decay
braam_sig = 0.45 * np.sin(2 * np.pi * b_freq * bt) + \
            0.25 * np.sin(2 * np.pi * 2 * b_freq * bt) + \
            0.15 * np.tanh(2.0 * np.sin(2 * np.pi * 3 * b_freq * bt))
braam[b_start:b_end] = braam_sig * b_env

# 5. UI High-Tech Telemetry Chirps (scanners locking on Jake & agents)
ui_fx = np.zeros(total_samples)
chirp_times = [0.8, 1.2, 4.2, 4.8, 5.4, 8.4]
for ct in chirp_times:
    c_start = int(ct * SAMPLE_RATE)
    c_len = int(0.08 * SAMPLE_RATE)
    c_end = min(c_start + c_len, total_samples)
    clen = c_end - c_start
    c_t = np.linspace(0, clen / SAMPLE_RATE, clen)
    # Double chirp
    chirp = 0.08 * np.sin(2 * np.pi * (1800 + 400 * np.sin(2 * np.pi * 40 * c_t)) * c_t) * np.exp(-c_t * 30.0)
    ui_fx[c_start:c_end] += chirp

# Master Mix
mix = drone + arp + whoosh + braam + ui_fx
# Normalize to avoid clipping
max_val = np.max(np.abs(mix))
if max_val > 0.95:
    mix = mix * (0.92 / max_val)

# Fade out last 0.8s
fade_out_samples = int(0.8 * SAMPLE_RATE)
fade = np.linspace(1.0, 0.0, fade_out_samples)
mix[-fade_out_samples:] *= fade

# Convert to 16-bit PCM stereo
left = mix * 0.98
right = mix * 0.98
stereo = np.vstack((left, right)).T
stereo_int16 = (stereo * 32767).astype(np.int16)

out_wav = "/Users/openclaw111/portfolio/fleet/assets/video/superhero_soundtrack.wav"
wavfile.write(out_wav, SAMPLE_RATE, stereo_int16)
print(f"Generated soundtrack: {out_wav} (size: {os.path.getsize(out_wav)} bytes)")
