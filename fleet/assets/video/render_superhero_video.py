import os
import sys
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.io import wavfile
import subprocess

FPS = 30
WIDTH = 1280
HEIGHT = 720
DURATION = 12.0
TOTAL_FRAMES = int(DURATION * FPS)
ASSETS_DIR = "/Users/openclaw111/portfolio/fleet/assets/video"

# 1. Synthesize Audio Soundtrack
print("Synthesizing cinematic audio soundtrack...")
SAMPLE_RATE = 44100
total_samples = int(SAMPLE_RATE * DURATION)
t = np.linspace(0, DURATION, total_samples, endpoint=False)

drone_freq = 55.0
drone = 0.35 * np.sin(2 * np.pi * drone_freq * t) + \
        0.18 * np.sin(2 * np.pi * (drone_freq * 2) * t) + \
        0.08 * np.sin(2 * np.pi * (drone_freq * 3) * t)
lfo = 0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t)
drone = drone * lfo

arp = np.zeros(total_samples)
bpm = 120.0
step_len = int(SAMPLE_RATE * 60.0 / bpm / 2)
notes = [220.0, 330.0, 440.0, 330.0, 220.0, 330.0, 523.25, 330.0,
         174.6, 261.6, 349.2, 261.6, 196.0, 293.6, 392.0, 293.6]
note_idx = 0
for start in range(0, total_samples, step_len):
    end = min(start + step_len, total_samples)
    seg_len = end - start
    st = np.linspace(0, seg_len / SAMPLE_RATE, seg_len, endpoint=False)
    freq = notes[note_idx % len(notes)]
    env = np.exp(-st * 12.0)
    synth = 0.12 * (np.sin(2 * np.pi * freq * st) + 0.5 * np.sin(2 * np.pi * 2 * freq * st)) * env
    arp[start:end] += synth
    note_idx += 1

whoosh = np.zeros(total_samples)
for wt in [3.6, 7.6]:
    w_start = int((wt - 0.4) * SAMPLE_RATE)
    w_end = int((wt + 0.6) * SAMPLE_RATE)
    w_len = w_end - w_start
    w_t = np.linspace(0, 1.0, w_len)
    noise = np.random.uniform(-1, 1, w_len)
    env = np.sin(np.pi * w_t)**2
    pitch_sweep = np.sin(2 * np.pi * (150 + 800 * (w_t**2)) * w_t)
    whoosh[w_start:w_end] += 0.25 * env * (0.6 * noise + 0.4 * pitch_sweep)

braam = np.zeros(total_samples)
b_start = int(7.7 * SAMPLE_RATE)
b_len = int(3.8 * SAMPLE_RATE)
b_end = min(b_start + b_len, total_samples)
actual_len = b_end - b_start
bt = np.linspace(0, actual_len / SAMPLE_RATE, actual_len, endpoint=False)
b_freq = 48.0 * np.exp(-bt * 0.15)
b_env = np.exp(-bt * 1.1) * (1.0 - np.exp(-bt * 30.0))
braam_sig = 0.48 * np.sin(2 * np.pi * b_freq * bt) + \
            0.28 * np.sin(2 * np.pi * 2 * b_freq * bt) + \
            0.18 * np.tanh(2.5 * np.sin(2 * np.pi * 3 * b_freq * bt))
braam[b_start:b_end] = braam_sig * b_env

ui_fx = np.zeros(total_samples)
for ct in [0.6, 1.1, 4.0, 4.6, 5.2, 8.2]:
    c_start = int(ct * SAMPLE_RATE)
    c_len = int(0.08 * SAMPLE_RATE)
    c_end = min(c_start + c_len, total_samples)
    clen = c_end - c_start
    c_t = np.linspace(0, clen / SAMPLE_RATE, clen)
    chirp = 0.08 * np.sin(2 * np.pi * (1800 + 400 * np.sin(2 * np.pi * 40 * c_t)) * c_t) * np.exp(-c_t * 30.0)
    ui_fx[c_start:c_end] += chirp

mix = drone + arp + whoosh + braam + ui_fx
max_val = np.max(np.abs(mix))
if max_val > 0.95:
    mix = mix * (0.92 / max_val)

fade_out_samples = int(0.8 * SAMPLE_RATE)
fade = np.linspace(1.0, 0.0, fade_out_samples)
mix[-fade_out_samples:] *= fade

stereo = np.vstack((mix * 0.98, mix * 0.98)).T
stereo_int16 = (stereo * 32767).astype(np.int16)
audio_path = os.path.join(ASSETS_DIR, "superhero_soundtrack.wav")
wavfile.write(audio_path, SAMPLE_RATE, stereo_int16)
print("Soundtrack generated successfully.")

# 2. Load Base Images
print("Loading base keyframes...")
img1_raw = Image.open(os.path.join(ASSETS_DIR, "hallway_scene1_lead.jpg")).convert("RGB")
img2_raw = Image.open(os.path.join(ASSETS_DIR, "hallway_scene2_stride.jpg")).convert("RGB")
img3_raw = Image.open(os.path.join(ASSETS_DIR, "hallway_scene3_climax.jpg")).convert("RGB")

# Pre-scale to standard 16:9 canvas with slight margin for camera movements
BASE_W, BASE_H = 1440, 810
img1 = img1_raw.resize((BASE_W, BASE_H), Image.Resampling.LANCZOS)
img2 = img2_raw.resize((BASE_W, BASE_H), Image.Resampling.LANCZOS)
img3 = img3_raw.resize((BASE_W, BASE_H), Image.Resampling.LANCZOS)

# Fonts
font_sans_bold = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22)
font_sans_sm = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 13)
font_sans_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 32)
font_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
font_mono_bold = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)

def crop_and_pan(img, zoom, center_x, center_y, sway_x=0.0, sway_y=0.0):
    """Crops with zoom, center anchor, and camera sway to output (WIDTH, HEIGHT)"""
    crop_w = BASE_W / zoom
    crop_h = BASE_H / zoom
    cx = BASE_W * center_x + sway_x
    cy = BASE_H * center_y + sway_y
    left = max(0, min(BASE_W - crop_w, cx - crop_w / 2))
    top = max(0, min(BASE_H - crop_h, cy - crop_h / 2))
    box = (int(left), int(top), int(left + crop_w), int(top + crop_h))
    return img.crop(box).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

def draw_hud(draw, frame_idx, t, scene_idx):
    # Top Telemetry Header
    draw.rectangle([(24, 20), (WIDTH - 24, 48)], fill=(10, 15, 25, 140))
    draw.line([(24, 48), (WIDTH - 24, 48)], fill=(0, 240, 255, 160), width=1)
    
    # Blinking status dot
    dot_color = (0, 255, 180) if (frame_idx // 15) % 2 == 0 else (0, 180, 255)
    draw.ellipse([(36, 30), (44, 38)], fill=dot_color)
    draw.text((54, 27), "WORKS4YOU AUTONOMOUS FLEET // LIVE MISSION PROTOCOL", fill=(240, 245, 255), font=font_mono_bold)
    
    time_str = f"T+{t:04.2f}s | 60 FPS | LATENCY: 9ms"
    draw.text((WIDTH - 280, 27), time_str, fill=(0, 240, 255), font=font_mono)

    # Corner brackets (Cyber frame)
    bracket_len = 35
    b_color = (0, 230, 255, 180)
    # Top-Left
    draw.line([(24, 20), (24 + bracket_len, 20)], fill=b_color, width=2)
    draw.line([(24, 20), (24, 20 + bracket_len)], fill=b_color, width=2)
    # Top-Right
    draw.line([(WIDTH - 24 - bracket_len, 20), (WIDTH - 24, 20)], fill=b_color, width=2)
    draw.line([(WIDTH - 24, 20), (WIDTH - 24, 20 + bracket_len)], fill=b_color, width=2)
    # Bottom-Left
    draw.line([(24, HEIGHT - 20), (24 + bracket_len, HEIGHT - 20)], fill=b_color, width=2)
    draw.line([(24, HEIGHT - 20), (24, HEIGHT - 20 - bracket_len)], fill=b_color, width=2)
    # Bottom-Right
    draw.line([(WIDTH - 24 - bracket_len, HEIGHT - 20), (WIDTH - 24, HEIGHT - 20)], fill=b_color, width=2)
    draw.line([(WIDTH - 24, HEIGHT - 20), (WIDTH - 24, HEIGHT - 20 - bracket_len)], fill=b_color, width=2)

    # Dynamic Scene-specific Elements
    if scene_idx == 1:
        # Jake Lock Reticle
        rx, ry = 640, 320
        rad = 60 + int(math.sin(t * 8) * 4)
        draw.ellipse([(rx - rad, ry - rad), (rx + rad, ry + rad)], outline=(0, 240, 255, 160), width=1)
        draw.line([(rx - rad - 15, ry), (rx - rad + 5, ry)], fill=(0, 240, 255), width=2)
        draw.line([(rx + rad - 5, ry), (rx + rad + 15, ry)], fill=(0, 240, 255), width=2)
        draw.line([(rx, ry - rad - 15), (rx, ry - rad + 5)], fill=(0, 240, 255), width=2)
        draw.line([(rx, ry + rad - 5), (rx, ry + rad + 15)], fill=(0, 240, 255), width=2)
        
        # Tag over Jake
        tag_x, tag_y = rx + rad + 15, ry - 30
        draw.rectangle([(tag_x, tag_y), (tag_x + 230, tag_y + 44)], fill=(12, 18, 32, 200), outline=(0, 240, 255), width=1)
        draw.text((tag_x + 10, tag_y + 6), "COMMANDER: JAKE", fill=(255, 255, 255), font=font_sans_bold)
        draw.text((tag_x + 10, tag_y + 26), "CHIEF ARCHITECT // IN STRIDE", fill=(0, 240, 255), font=font_mono)

    elif scene_idx == 2:
        # Squad assembling & interacting - Multiple Specialist Tags
        tags = [
            (280, 280, "KATIE", "COMMERCE & ADS"),
            (560, 250, "JAKE & CLAIRE", "COMMAND & SYNC"),
            (950, 300, "WARREN & VANCE", "FINANCE & SECURITY")
        ]
        for tx, ty, name, role in tags:
            # Subtle floating tag
            draw.rectangle([(tx, ty), (tx + 190, ty + 38)], fill=(10, 16, 28, 190), outline=(100, 200, 255, 180), width=1)
            draw.text((tx + 8, ty + 4), name, fill=(255, 255, 255), font=font_sans_sm)
            draw.text((tx + 8, ty + 20), role, fill=(0, 230, 255), font=font_mono)
            draw.line([(tx, ty + 19), (tx - 12, ty + 25)], fill=(0, 230, 255, 160), width=1)

    elif scene_idx == 3:
        # Climax Banner - The Confident Halt
        banner_w, banner_h = 680, 80
        bx = (WIDTH - banner_w) // 2
        by = HEIGHT - 130
        draw.rectangle([(bx, by), (bx + banner_w, by + banner_h)], fill=(8, 12, 22, 220), outline=(0, 240, 255, 220), width=2)
        # Glowing inner border
        draw.rectangle([(bx + 3, by + 3), (bx + banner_w - 3, by + banner_h - 3)], outline=(0, 160, 255, 100), width=1)
        
        draw.text((bx + 25, by + 12), "WORKS4YOU AUTONOMOUS FLEET", fill=(255, 255, 255), font=font_sans_title)
        draw.text((bx + 25, by + 48), "9 SPECIALISTS. SYNCHRONIZED EXECUTION. ZERO LATENCY.", fill=(0, 240, 255), font=font_mono_bold)

# 3. Setup FFmpeg Pipe
output_mp4 = os.path.join(ASSETS_DIR, "fleet_superhero_hallway.mp4")
poster_path = os.path.join(ASSETS_DIR, "fleet_superhero_poster.jpg")

cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",  # Video input from pipe
    "-i", audio_path, # Audio input
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-movflags", "+faststart",
    output_mp4
]

print(f"Starting video encoding to {output_mp4}...")
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

for f in range(TOTAL_FRAMES):
    t = f / FPS
    
    # Determine active scene & transition weights
    # Scene 1: 0.0s to 3.8s (frames 0 to 114)
    # Transition 1: 3.4s to 4.0s (frames 102 to 120)
    # Scene 2: 3.8s to 7.8s (frames 114 to 234)
    # Transition 2: 7.4s to 8.0s (frames 222 to 240)
    # Scene 3: 7.8s to 12.0s (frames 234 to 360)
    
    sway_step = math.sin(t * 3.6 * 2 * math.pi) * 3.0
    sway_bob = abs(math.sin(t * 3.6 * 2 * math.pi)) * 3.5

    if t < 3.4:
        # Pure Scene 1
        scene_idx = 1
        zoom = 1.02 + (t / 3.8) * 0.12
        frame_img = crop_and_pan(img1, zoom, 0.49, 0.49, sway_step, sway_bob)
    elif t < 4.0:
        # Crossfade Scene 1 -> Scene 2
        scene_idx = 2
        alpha = (t - 3.4) / 0.6
        z1 = 1.02 + (t / 3.8) * 0.12
        f1 = crop_and_pan(img1, z1, 0.49, 0.49, sway_step, sway_bob)
        t_s2 = t - 3.4
        z2 = 1.08 + (t_s2 / 4.0) * 0.05
        f2 = crop_and_pan(img2, z2, 0.45 + (t_s2 / 4.0) * 0.08, 0.50, sway_step, sway_bob)
        frame_img = Image.blend(f1, f2, alpha)
    elif t < 7.4:
        # Pure Scene 2
        scene_idx = 2
        t_s2 = t - 3.4
        zoom = 1.08 + (t_s2 / 4.0) * 0.05
        cx = 0.45 + (t_s2 / 4.0) * 0.08
        frame_img = crop_and_pan(img2, zoom, cx, 0.50, sway_step, sway_bob)
    elif t < 8.0:
        # Crossfade Scene 2 -> Scene 3
        scene_idx = 3
        alpha = (t - 7.4) / 0.6
        t_s2 = t - 3.4
        z2 = 1.08 + (t_s2 / 4.0) * 0.05
        cx = 0.45 + (t_s2 / 4.0) * 0.08
        f2 = crop_and_pan(img2, z2, cx, 0.50, sway_step, sway_bob)
        t_s3 = t - 7.4
        z3 = 1.03 + (t_s3 / 4.6) * 0.08
        f3 = crop_and_pan(img3, z3, 0.50, 0.46, 0.0, math.sin(t_s3 * 1.2) * 1.5)
        frame_img = Image.blend(f2, f3, alpha)
    else:
        # Pure Scene 3 - Climax Hero Halt & Stare
        scene_idx = 3
        t_s3 = t - 7.4
        # Slow dramatic confident push-in
        zoom = 1.03 + (t_s3 / 4.6) * 0.08
        frame_img = crop_and_pan(img3, zoom, 0.50, 0.46, 0.0, math.sin(t_s3 * 1.2) * 1.5)

    # Render HUD & Graphics
    draw = ImageDraw.Draw(frame_img, "RGBA")
    draw_hud(draw, f, t, scene_idx)
    
    # Save poster frame at t=9.5s
    if f == int(9.5 * FPS):
        frame_img.convert("RGB").save(poster_path, quality=95)
        print(f"Saved poster frame to {poster_path}")

    # Write raw bytes to FFmpeg stdin
    proc.stdin.write(frame_img.convert("RGB").tobytes())
    
    if f % 60 == 0:
        print(f"Rendered {f}/{TOTAL_FRAMES} frames ({t:04.1f}s)...")

proc.stdin.close()
proc.wait()
print(f"Video compilation completed: {output_mp4} (size: {os.path.getsize(output_mp4)} bytes)")
