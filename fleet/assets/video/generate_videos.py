import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/Users/openclaw111/portfolio/fleet/assets/video"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fonts
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def get_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def create_circular_avatar(img_path, size):
    try:
        im = Image.open(img_path).convert("RGBA")
        im = im.resize((size, size), Image.Resampling.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        output.paste(im, (0, 0), mask=mask)
        return output
    except Exception as e:
        print(f"Error loading avatar {img_path}: {e}")
        fallback = Image.new("RGBA", (size, size), (56, 189, 248, 255))
        return fallback

# --- 1. Edith Ltd Legal UGC Reel ---
def generate_edith_legal_reel():
    print("Generating Edith Legal UGC reel...")
    width, height = 540, 960
    fps = 30
    duration_sec = 6
    total_frames = fps * duration_sec
    temp_frames_dir = os.path.join(OUTPUT_DIR, "tmp_edith")
    os.makedirs(temp_frames_dir, exist_ok=True)

    idit_avatar = create_circular_avatar("/Users/openclaw111/portfolio/idit/profile.jpg", 72)
    maya_avatar = create_circular_avatar("/Users/openclaw111/portfolio/fleet/assets/transparent/claire_transparent.png", 64)

    for i in range(total_frames):
        t = i / total_frames
        im = Image.new("RGBA", (width, height), (15, 12, 28, 255))
        draw = ImageDraw.Draw(im)

        # Ambient gradient background
        for y in range(height):
            ratio = y / height
            r = int(18 + 15 * math.sin(t * 2 * math.pi + ratio * 3))
            g = int(12 + 10 * math.cos(t * 2 * math.pi + ratio * 2))
            b = int(35 + 25 * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # Top Header: UGC Creator info
        draw_rounded_rect(draw, (16, 24, width - 16, 116), radius=18, fill=(30, 22, 54, 220), outline=(147, 51, 234, 180), width=1)
        im.paste(idit_avatar, (28, 34), idit_avatar)
        
        # Online pulse dot
        pulse_r = int(5 + 2 * math.sin(i * 0.4))
        draw.ellipse((86 - pulse_r, 92 - pulse_r, 86 + pulse_r, 92 + pulse_r), fill=(34, 197, 94, 255))

        draw.text((112, 38), "Idit Snir • Legal Partner", font=get_font(16, bold=True), fill=(255, 255, 255, 255))
        draw.text((112, 60), "@edith_snir_law • Edith Ltd Legal", font=get_font(12), fill=(192, 132, 252, 255))
        draw.text((112, 80), "Verified AI Law Practice • Tel Aviv", font=get_font(11), fill=(148, 163, 184, 255))

        # UGC Tag pill
        draw_rounded_rect(draw, (width - 130, 36, width - 28, 62), radius=12, fill=(147, 51, 234, 220))
        draw.text((width - 118, 42), "⚡ LIVE UGC", font=get_font(11, bold=True), fill=(255, 255, 255, 255))

        # Quote Bubble
        draw_rounded_rect(draw, (20, 130, width - 20, 220), radius=16, fill=(45, 33, 78, 200), outline=(168, 85, 247, 100), width=1)
        draw.text((36, 142), "\"Maya audited 42 alimony clauses in 1.4s,", font=get_font(15, bold=True), fill=(255, 255, 255, 255))
        draw.text((36, 168), "corrected CPI deviation, and staged the", font=get_font(15, bold=True), fill=(255, 255, 255, 255))
        draw.text((36, 194), "court redlines for my 1-click digital sign-off!\"", font=get_font(15, bold=True), fill=(56, 189, 248, 255))

        # Middle Execution Window (The AI Workstation)
        win_y1 = 236
        win_y2 = 680
        draw_rounded_rect(draw, (18, win_y1, width - 18, win_y2), radius=20, fill=(10, 8, 20, 245), outline=(147, 51, 234, 180), width=2)

        # Window Header
        draw_rounded_rect(draw, (18, win_y1, width - 18, win_y1 + 44), radius=20, fill=(24, 18, 44, 255))
        draw.line([(18, win_y1 + 44), (width - 18, win_y1 + 44)], fill=(147, 51, 234, 80), width=1)
        
        # Dots
        draw.ellipse((34, win_y1 + 16, 44, win_y1 + 26), fill=(239, 68, 68, 255))
        draw.ellipse((52, win_y1 + 16, 62, win_y1 + 26), fill=(245, 158, 11, 255))
        draw.ellipse((70, win_y1 + 16, 80, win_y1 + 26), fill=(34, 197, 94, 255))
        draw.text((96, win_y1 + 14), "Maya Legal Pod v2.8 • Actuarial Engine", font=get_font(12, bold=True), fill=(226, 232, 240, 255))

        # Agent mini card inside window
        im.paste(maya_avatar, (32, win_y1 + 56), maya_avatar)
        draw.text((106, win_y1 + 62), "Maya — Autonomous Corporate Counsel", font=get_font(13, bold=True), fill=(255, 255, 255, 255))
        draw.text((106, win_y1 + 82), "Status: Real-time Court Audit Active (142ms)", font=get_font(11), fill=(56, 189, 248, 255))

        # Terminal Lines
        code_lines = [
            (">> INGEST: Supreme Court Family Mandate #2049.pdf", (148, 163, 184)),
            (">> OCR: Extracted 42 liability & retroactive clauses", (148, 163, 184)),
            (">> CPI CALCULATION: 3.8% compound inflation drift", (245, 158, 11)),
            (">> ARREARS REBALANCED: ₪184,250 ILS ($49,850 USD)", (34, 197, 94)),
            (">> DRAFT: Annex G-4 structured with Israeli legal code", (192, 132, 252)),
            (">> STAGING: Cryptographic Human Gate Awaiting Signature", (56, 189, 248)),
        ]
        
        # Progressive appearance of lines based on time
        visible_count = min(len(code_lines), int(t * len(code_lines) * 1.5) + 1)
        line_y = win_y1 + 130
        for idx in range(visible_count):
            txt, color = code_lines[idx]
            draw.text((34, line_y), txt, font=get_font(11, bold=True), fill=color)
            line_y += 26

        # Animated Laser Scanline
        scan_y = win_y1 + 120 + int((win_y2 - win_y1 - 180) * ((t * 2) % 1.0))
        draw.line([(24, scan_y), (width - 24, scan_y)], fill=(56, 189, 248, 200), width=2)
        # Scan glow
        draw.line([(24, scan_y - 1), (width - 24, scan_y - 1)], fill=(56, 189, 248, 80), width=1)
        draw.line([(24, scan_y + 1), (width - 24, scan_y + 1)], fill=(56, 189, 248, 80), width=1)

        # Cryptographic Approval Gate Badge
        gate_pulse = 0.5 + 0.5 * math.sin(i * 0.3)
        gate_border_alpha = int(150 + 105 * gate_pulse)
        draw_rounded_rect(draw, (32, win_y2 - 130, width - 32, win_y2 - 20), radius=14, 
                          fill=(20, 15, 38, 240), outline=(56, 189, 248, gate_border_alpha), width=2)
        draw.text((46, win_y2 - 118), "🛡️ CRYPTOGRAPHIC APPROVAL GATE", font=get_font(12, bold=True), fill=(56, 189, 248, 255))
        draw.text((46, win_y2 - 94), "Status: 1-Click Signature Ready for Idit Snir", font=get_font(11), fill=(255, 255, 255, 255))
        
        # Approve button simulation
        draw_rounded_rect(draw, (width - 170, win_y2 - 76, width - 46, win_y2 - 34), radius=10, fill=(34, 197, 94, 255))
        draw.text((width - 156, win_y2 - 64), "✓ Sign & File", font=get_font(12, bold=True), fill=(255, 255, 255, 255))

        # Bottom UGC Info & Captions
        caption_y = 700
        draw.text((24, caption_y), "@edith_snir_law", font=get_font(16, bold=True), fill=(255, 255, 255, 255))
        draw.text((24, caption_y + 24), "How Edith Ltd Legal scaled 4x without junior associates.", font=get_font(13), fill=(226, 232, 240, 255))
        draw.text((24, caption_y + 44), "#LegalAI #AutonomousFleet #Works4you #GoogleADK", font=get_font(12), fill=(192, 132, 252, 255))

        # Animated Audio Frequency Wave
        wave_x = 24
        wave_y = caption_y + 78
        draw.text((wave_x, wave_y - 2), "🎵 Works4you Audio • Maya Voice 2.8", font=get_font(11), fill=(148, 163, 184, 255))
        for bar_idx in range(16):
            bar_h = int(6 + 12 * abs(math.sin(i * 0.35 + bar_idx * 0.5)))
            bx = wave_x + 230 + bar_idx * 6
            draw.line([(bx, wave_y + 8 - bar_h // 2), (bx, wave_y + 8 + bar_h // 2)], fill=(56, 189, 248, 240), width=3)

        # Right Side UGC Floating Reaction Pill Icons
        reactions = [
            ("❤️", "2.8k", 740),
            ("💬", "342", 796),
            ("🔖", "891", 852),
        ]
        rx = width - 42
        for icon, count, ry in reactions:
            draw.ellipse((rx - 18, ry - 18, rx + 18, ry + 18), fill=(30, 22, 54, 200), outline=(255, 255, 255, 60), width=1)
            draw.text((rx - 10, ry - 12), icon, font=get_font(14), fill=(255, 255, 255, 255))
            draw.text((rx - 14, ry + 14), count, font=get_font(9, bold=True), fill=(226, 232, 240, 255))

        # Bottom Progress Bar
        draw.rectangle([(0, height - 6), (width, height)], fill=(40, 30, 60, 255))
        draw.rectangle([(0, height - 6), (int(width * t), height)], fill=(168, 85, 247, 255))

        frame_path = os.path.join(temp_frames_dir, f"frame_{i:04d}.png")
        im.save(frame_path)

    # Encode with ffmpeg
    out_mp4 = os.path.join(OUTPUT_DIR, "ugc_edith_legal.mp4")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-crf", "22",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Cleanup temp frames
    for f in os.listdir(temp_frames_dir):
        os.remove(os.path.join(temp_frames_dir, f))
    os.rmdir(temp_frames_dir)
    print(f"Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")

# --- 2. Forest for All (4rest4all) UGC Reel ---
def generate_4rest_reel():
    print("Generating 4rest4all UGC reel...")
    width, height = 540, 960
    fps = 30
    duration_sec = 6
    total_frames = fps * duration_sec
    temp_frames_dir = os.path.join(OUTPUT_DIR, "tmp_4rest")
    os.makedirs(temp_frames_dir, exist_ok=True)

    katie_avatar = create_circular_avatar("/Users/openclaw111/portfolio/fleet/assets/transparent/katie_transparent.png", 72)
    forest_cover = Image.open("/Users/openclaw111/portfolio/cover-4rest4all.png").convert("RGBA")
    forest_cover = forest_cover.resize((width - 40, 110), Image.Resampling.LANCZOS)

    for i in range(total_frames):
        t = i / total_frames
        im = Image.new("RGBA", (width, height), (8, 24, 18, 255))
        draw = ImageDraw.Draw(im)

        # Ambient green/teal gradient
        for y in range(height):
            ratio = y / height
            r = int(8 + 8 * math.sin(t * 2 * math.pi + ratio * 2))
            g = int(24 + 18 * ratio)
            b = int(20 + 15 * math.cos(t * 2 * math.pi + ratio * 3))
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # Top Header
        draw_rounded_rect(draw, (16, 24, width - 16, 116), radius=18, fill=(16, 42, 32, 220), outline=(34, 197, 94, 180), width=1)
        im.paste(katie_avatar, (28, 34), katie_avatar)

        # Online pulse dot
        pulse_r = int(5 + 2 * math.sin(i * 0.4))
        draw.ellipse((86 - pulse_r, 92 - pulse_r, 86 + pulse_r, 92 + pulse_r), fill=(34, 197, 94, 255))

        draw.text((112, 38), "Forest for All • 4rest4all", font=get_font(16, bold=True), fill=(255, 255, 255, 255))
        draw.text((112, 60), "@4rest4all_org • NGO Field Intelligence", font=get_font(12), fill=(134, 239, 172, 255))
        draw.text((112, 80), "Multilingual Donor Engagement • 3 Continents", font=get_font(11), fill=(148, 163, 184, 255))

        # UGC Tag pill
        draw_rounded_rect(draw, (width - 130, 36, width - 28, 62), radius=12, fill=(34, 197, 94, 220))
        draw.text((width - 118, 42), "🌿 LIVE UGC", font=get_font(11, bold=True), fill=(255, 255, 255, 255))

        # Quote Bubble
        draw_rounded_rect(draw, (20, 130, width - 20, 220), radius=16, fill=(20, 56, 42, 200), outline=(34, 197, 94, 100), width=1)
        draw.text((36, 142), "\"Our autonomous agent engaged 1,400 donors", font=get_font(15, bold=True), fill=(255, 255, 255, 255))
        draw.text((36, 168), "in 4 languages and dispatched Stripe links", font=get_font(15, bold=True), fill=(255, 255, 255, 255))
        draw.text((36, 194), "while our conservationists planted 20K trees!\"", font=get_font(15, bold=True), fill=(52, 211, 153, 255))

        # Middle Execution Window (Chat + Geospatial CRM)
        win_y1 = 236
        win_y2 = 680
        draw_rounded_rect(draw, (18, win_y1, width - 18, win_y2), radius=20, fill=(10, 28, 22, 245), outline=(34, 197, 94, 180), width=2)

        # Header
        draw_rounded_rect(draw, (18, win_y1, width - 18, win_y1 + 44), radius=20, fill=(16, 44, 34, 255))
        draw.line([(18, win_y1 + 44), (width - 18, win_y1 + 44)], fill=(34, 197, 94, 80), width=1)
        draw.ellipse((34, win_y1 + 16, 44, win_y1 + 26), fill=(239, 68, 68, 255))
        draw.ellipse((52, win_y1 + 16, 62, win_y1 + 26), fill=(245, 158, 11, 255))
        draw.ellipse((70, win_y1 + 16, 80, win_y1 + 26), fill=(34, 197, 94, 255))
        draw.text((96, win_y1 + 14), "4rest Scout & Advocate Engine • Port 9222", font=get_font(12, bold=True), fill=(226, 232, 240, 255))

        # Inset cover banner
        im.paste(forest_cover, (20, win_y1 + 52), forest_cover)

        # Simulated Chat Stream
        chat_y = win_y1 + 175
        # Donor Bubble (Left)
        draw_rounded_rect(draw, (32, chat_y, 380, chat_y + 60), radius=12, fill=(24, 60, 48, 240))
        draw.text((44, chat_y + 10), "🇧🇷 Donor (São Paulo, Instagram DM):", font=get_font(11, bold=True), fill=(134, 239, 172, 255))
        draw.text((44, chat_y + 28), "\"Olá! Quero apoiar o plantio no Pará.\"", font=get_font(13), fill=(255, 255, 255, 255))

        # Agent Response Bubble (Right)
        resp_y = chat_y + 72
        draw_rounded_rect(draw, (90, resp_y, width - 32, resp_y + 80), radius=12, fill=(16, 75, 52, 255), outline=(52, 211, 153, 180), width=1)
        draw.text((104, resp_y + 10), "⚡ 4rest Advocate (140ms Latency):", font=get_font(11, bold=True), fill=(52, 211, 153, 255))
        draw.text((104, resp_y + 28), "\"Parabéns! Cada R$ 50 planta 2 árvores nativas.", font=get_font(12), fill=(255, 255, 255, 255))
        draw.text((104, resp_y + 48), "Link oficial Stripe gerado para o Pará:\"", font=get_font(12), fill=(255, 255, 255, 255))

        # Stripe Interactive Card Inset
        stripe_y = resp_y + 92
        draw_rounded_rect(draw, (32, stripe_y, width - 32, win_y2 - 20), radius=14, fill=(8, 38, 28, 255), outline=(34, 197, 94, 220), width=2)
        draw.text((48, stripe_y + 14), "💳 STRIPE INSTANT CHECKOUT READY", font=get_font(12, bold=True), fill=(52, 211, 153, 255))
        draw.text((48, stripe_y + 36), "Allocation: Pará Native Reforestation #782", font=get_font(11), fill=(226, 232, 240, 255))
        draw.text((48, stripe_y + 54), "Twenty CRM Sync: Lead Created & Tagged [Donor_Active]", font=get_font(11), fill=(148, 163, 184, 255))

        # Bottom UGC Info & Captions
        caption_y = 700
        draw.text((24, caption_y), "@4rest4all_org", font=get_font(16, bold=True), fill=(255, 255, 255, 255))
        draw.text((24, caption_y + 24), "Global NGO automation: 24/7 multilingual qualification.", font=get_font(13), fill=(226, 232, 240, 255))
        draw.text((24, caption_y + 44), "#ClimateTech #Rainforest #Stripe #TwentyCRM", font=get_font(12), fill=(134, 239, 172, 255))

        # Frequency Wave
        wave_x = 24
        wave_y = caption_y + 78
        draw.text((wave_x, wave_y - 2), "🎵 Works4you Audio • Portuguese RAG 2.8", font=get_font(11), fill=(148, 163, 184, 255))
        for bar_idx in range(16):
            bar_h = int(6 + 12 * abs(math.sin(i * 0.35 + bar_idx * 0.5)))
            bx = wave_x + 230 + bar_idx * 6
            draw.line([(bx, wave_y + 8 - bar_h // 2), (bx, wave_y + 8 + bar_h // 2)], fill=(34, 197, 94, 240), width=3)

        # Reactions
        reactions = [
            ("❤️", "3.4k", 740),
            ("💬", "512", 796),
            ("🔖", "1.4k", 852),
        ]
        rx = width - 42
        for icon, count, ry in reactions:
            draw.ellipse((rx - 18, ry - 18, rx + 18, ry + 18), fill=(20, 50, 36, 200), outline=(255, 255, 255, 60), width=1)
            draw.text((rx - 10, ry - 12), icon, font=get_font(14), fill=(255, 255, 255, 255))
            draw.text((rx - 14, ry + 14), count, font=get_font(9, bold=True), fill=(226, 232, 240, 255))

        # Bottom Progress Bar
        draw.rectangle([(0, height - 6), (width, height)], fill=(20, 48, 36, 255))
        draw.rectangle([(0, height - 6), (int(width * t), height)], fill=(34, 197, 94, 255))

        frame_path = os.path.join(temp_frames_dir, f"frame_{i:04d}.png")
        im.save(frame_path)

    # Encode
    out_mp4 = os.path.join(OUTPUT_DIR, "ugc_4rest4all.mp4")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-crf", "22",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for f in os.listdir(temp_frames_dir):
        os.remove(os.path.join(temp_frames_dir, f))
    os.rmdir(temp_frames_dir)
    print(f"Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")

# --- 3. Founder Operations & Cashflow UGC Reel ---
def generate_founder_cashflow_reel():
    print("Generating Founder Cashflow UGC reel...")
    width, height = 540, 960
    fps = 30
    duration_sec = 6
    total_frames = fps * duration_sec
    temp_frames_dir = os.path.join(OUTPUT_DIR, "tmp_founder")
    os.makedirs(temp_frames_dir, exist_ok=True)

    shimon_avatar = create_circular_avatar("/Users/openclaw111/portfolio/profile.jpg", 72)
    warren_avatar = create_circular_avatar("/Users/openclaw111/portfolio/fleet/assets/transparent/warren_transparent.png", 64)

    for i in range(total_frames):
        t = i / total_frames
        im = Image.new("RGBA", (width, height), (12, 18, 32, 255))
        draw = ImageDraw.Draw(im)

        # Ambient navy/amber gradient
        for y in range(height):
            ratio = y / height
            r = int(12 + 10 * math.sin(t * 2 * math.pi + ratio * 2))
            g = int(18 + 14 * ratio)
            b = int(32 + 25 * math.cos(t * 2 * math.pi + ratio * 2))
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # Top Header
        draw_rounded_rect(draw, (16, 24, width - 16, 116), radius=18, fill=(20, 30, 52, 220), outline=(245, 158, 11, 180), width=1)
        im.paste(shimon_avatar, (28, 34), shimon_avatar)

        pulse_r = int(5 + 2 * math.sin(i * 0.4))
        draw.ellipse((86 - pulse_r, 92 - pulse_r, 86 + pulse_r, 92 + pulse_r), fill=(34, 197, 94, 255))

        draw.text((112, 38), "Shimon Ezekiel • Founder & COO", font=get_font(16, bold=True), fill=(255, 255, 255, 255))
        draw.text((112, 60), "@shimon_ezekiel • Works4you Fleet", font=get_font(12), fill=(251, 191, 36, 255))
        draw.text((112, 80), "Zero-Touch Executive Operations • 180ms", font=get_font(11), fill=(148, 163, 184, 255))

        # UGC Tag pill
        draw_rounded_rect(draw, (width - 130, 36, width - 28, 62), radius=12, fill=(245, 158, 11, 220))
        draw.text((width - 118, 42), "⚡ LIVE UGC", font=get_font(11, bold=True), fill=(255, 255, 255, 255))

        # Quote Bubble
        draw_rounded_rect(draw, (20, 130, width - 20, 220), radius=16, fill=(28, 42, 70, 200), outline=(245, 158, 11, 100), width=1)
        draw.text((36, 142), "\"14 multi-currency invoices arrived today.", font=get_font(15, bold=True), fill=(255, 255, 255, 255))
        draw.text((36, 168), "Warren converted EUR/ILS to USD and reconciled", font=get_font(15, bold=True), fill=(255, 255, 255, 255))
        draw.text((36, 194), "our Google Sheets cashflow without human touch!\"", font=get_font(15, bold=True), fill=(251, 191, 36, 255))

        # Middle Execution Window
        win_y1 = 236
        win_y2 = 680
        draw_rounded_rect(draw, (18, win_y1, width - 18, win_y2), radius=20, fill=(10, 18, 30, 245), outline=(245, 158, 11, 180), width=2)

        # Header
        draw_rounded_rect(draw, (18, win_y1, width - 18, win_y1 + 44), radius=20, fill=(18, 28, 46, 255))
        draw.line([(18, win_y1 + 44), (width - 18, win_y1 + 44)], fill=(245, 158, 11, 80), width=1)
        draw.ellipse((34, win_y1 + 16, 44, win_y1 + 26), fill=(239, 68, 68, 255))
        draw.ellipse((52, win_y1 + 16, 62, win_y1 + 26), fill=(245, 158, 11, 255))
        draw.ellipse((70, win_y1 + 16, 80, win_y1 + 26), fill=(34, 197, 94, 255))
        draw.text((96, win_y1 + 14), "Warren Treasury & FX Controller • ADK 2.8", font=get_font(12, bold=True), fill=(226, 232, 240, 255))

        im.paste(warren_avatar, (32, win_y1 + 56), warren_avatar)
        draw.text((106, win_y1 + 62), "Warren — Treasury & Financial Controller", font=get_font(13, bold=True), fill=(255, 255, 255, 255))
        draw.text((106, win_y1 + 82), "Status: Real-time FX Spot Rebalance Active (180ms)", font=get_font(11), fill=(251, 191, 36, 255))

        # Financial Ledger Lines
        fin_lines = [
            (">> INGEST: tecktitans111@gmail.com (Vertex AI invoice)", (148, 163, 184)),
            (">> AMOUNT: €3,420.00 EUR (Invoice #INV-88310)", (226, 232, 240)),
            (">> FX RATE: EUR/USD = 1.0842 • Converted: $3,707.96 USD", (245, 158, 11)),
            (">> RECONCILIATION: Google Sheets 'Cost Detail' Row #142", (34, 197, 94)),
            (">> MONTHLY SUMMARY: Budget Burn: 42.1% | Runway: 14.8 Mos", (56, 189, 248)),
            (">> NOTIFICATION: Chatwoot & Telegram Summary Dispatched", (192, 132, 252)),
        ]
        visible_count = min(len(fin_lines), int(t * len(fin_lines) * 1.5) + 1)
        line_y = win_y1 + 130
        for idx in range(visible_count):
            txt, color = fin_lines[idx]
            draw.text((34, line_y), txt, font=get_font(11, bold=True), fill=color)
            line_y += 26

        # Animated FX Candlestick Chart
        chart_y = win_y2 - 130
        draw_rounded_rect(draw, (32, chart_y, width - 32, win_y2 - 20), radius=14, fill=(16, 26, 44, 255), outline=(245, 158, 11, 200), width=1)
        draw.text((46, chart_y + 12), "📊 REAL-TIME MULTI-CURRENCY REBALANCE", font=get_font(12, bold=True), fill=(251, 191, 36, 255))
        
        # Draw mini graph bars
        for bar_idx in range(18):
            bx = 48 + bar_idx * 24
            base_h = 24 + 18 * math.sin(bar_idx * 0.4 + t * 4)
            draw.rectangle([(bx, chart_y + 80 - int(base_h)), (bx + 14, chart_y + 80)], fill=(34, 197, 94, 220))
        draw.text((48, chart_y + 88), "Net Burn Saved: $6,420/mo via Automated Spot Optimization", font=get_font(10), fill=(148, 163, 184, 255))

        # Bottom UGC Info & Captions
        caption_y = 700
        draw.text((24, caption_y), "@shimon_ezekiel", font=get_font(16, bold=True), fill=(255, 255, 255, 255))
        draw.text((24, caption_y + 24), "Autonomous founder operations: Zero manual bookkeeping.", font=get_font(13), fill=(226, 232, 240, 255))
        draw.text((24, caption_y + 44), "#BizOps #CashflowAI #FinTech #Works4you", font=get_font(12), fill=(251, 191, 36, 255))

        # Frequency Wave
        wave_x = 24
        wave_y = caption_y + 78
        draw.text((wave_x, wave_y - 2), "🎵 Works4you Audio • Treasury Matrix 2.8", font=get_font(11), fill=(148, 163, 184, 255))
        for bar_idx in range(16):
            bar_h = int(6 + 12 * abs(math.sin(i * 0.35 + bar_idx * 0.5)))
            bx = wave_x + 230 + bar_idx * 6
            draw.line([(bx, wave_y + 8 - bar_h // 2), (bx, wave_y + 8 + bar_h // 2)], fill=(245, 158, 11, 240), width=3)

        # Reactions
        reactions = [
            ("❤️", "4.1k", 740),
            ("💬", "488", 796),
            ("🔖", "1.2k", 852),
        ]
        rx = width - 42
        for icon, count, ry in reactions:
            draw.ellipse((rx - 18, ry - 18, rx + 18, ry + 18), fill=(28, 38, 60, 200), outline=(255, 255, 255, 60), width=1)
            draw.text((rx - 10, ry - 12), icon, font=get_font(14), fill=(255, 255, 255, 255))
            draw.text((rx - 14, ry + 14), count, font=get_font(9, bold=True), fill=(226, 232, 240, 255))

        # Bottom Progress Bar
        draw.rectangle([(0, height - 6), (width, height)], fill=(24, 34, 52, 255))
        draw.rectangle([(0, height - 6), (int(width * t), height)], fill=(245, 158, 11, 255))

        frame_path = os.path.join(temp_frames_dir, f"frame_{i:04d}.png")
        im.save(frame_path)

    # Encode
    out_mp4 = os.path.join(OUTPUT_DIR, "ugc_founder_cashflow.mp4")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-crf", "22",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for f in os.listdir(temp_frames_dir):
        os.remove(os.path.join(temp_frames_dir, f))
    os.rmdir(temp_frames_dir)
    print(f"Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")

# --- 4. Hero Ambient Futuristic Motion Loop ---
def generate_hero_ambient_video():
    print("Generating Hero Ambient Motion Loop...")
    width, height = 1280, 720
    fps = 30
    duration_sec = 6
    total_frames = fps * duration_sec
    temp_frames_dir = os.path.join(OUTPUT_DIR, "tmp_hero")
    os.makedirs(temp_frames_dir, exist_ok=True)

    brand_logo = Image.open("/Users/openclaw111/portfolio/fleet/assets/w4y_brand_lockup_3d_trans.png").convert("RGBA")
    logo_w, logo_h = 360, int(360 * brand_logo.height / brand_logo.width)
    brand_logo = brand_logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

    # Agent node positions in an oval
    center_x, center_y = width // 2, height // 2
    nodes = []
    num_nodes = 9
    for n in range(num_nodes):
        angle = n * 2 * math.pi / num_nodes
        nodes.append((angle, 380, 200)) # rx, ry

    for i in range(total_frames):
        t = i / total_frames
        im = Image.new("RGBA", (width, height), (10, 15, 29, 255))
        draw = ImageDraw.Draw(im)

        # Ambient flowing gradient mesh
        for y in range(0, height, 4):
            ratio = y / height
            r = int(10 + 12 * math.sin(t * 2 * math.pi + ratio * 3))
            g = int(14 + 16 * math.cos(t * 2 * math.pi + ratio * 2))
            b = int(28 + 35 * ratio)
            draw.rectangle([(0, y), (width, y + 4)], fill=(r, g, b, 255))

        # Connecting neural lines between nodes
        current_node_coords = []
        for angle, rx, ry in nodes:
            cur_angle = angle + t * 2 * math.pi * 0.2
            nx = center_x + int(rx * math.cos(cur_angle))
            ny = center_y + int(ry * math.sin(cur_angle))
            current_node_coords.append((nx, ny))

        # Draw mesh lines
        for j in range(num_nodes):
            x1, y1 = current_node_coords[j]
            x2, y2 = current_node_coords[(j + 1) % num_nodes]
            draw.line([(x1, y1), (x2, y2)], fill=(56, 189, 248, 60), width=1)
            # Cross lines
            x3, y3 = current_node_coords[(j + 3) % num_nodes]
            draw.line([(x1, y1), (x3, y3)], fill=(168, 85, 247, 40), width=1)
            # Center connect
            draw.line([(x1, y1), (center_x, center_y)], fill=(6, 182, 212, 35), width=1)

        # Floating glowing pulses along lines
        for j in range(num_nodes):
            x1, y1 = current_node_coords[j]
            x2, y2 = current_node_coords[(j + 1) % num_nodes]
            pulse_t = (t * 3 + j * 0.2) % 1.0
            px = int(x1 + (x2 - x1) * pulse_t)
            py = int(y1 + (y2 - y1) * pulse_t)
            draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=(56, 189, 248, 220))

        # Node circles
        for idx, (nx, ny) in enumerate(current_node_coords):
            nr = int(8 + 3 * math.sin(i * 0.2 + idx))
            draw.ellipse((nx - nr, ny - nr, nx + nr, ny + nr), fill=(34, 197, 94, 255))
            draw.ellipse((nx - nr - 3, ny - nr - 3, nx + nr + 3, ny + nr + 3), outline=(56, 189, 248, 120), width=2)

        # Center Emblem
        logo_x = center_x - logo_w // 2
        logo_y = center_y - logo_h // 2 + int(6 * math.sin(t * 2 * math.pi))
        im.paste(brand_logo, (logo_x, logo_y), brand_logo)

        # Subtle Telemetry Watermark text
        draw.text((36, height - 48), "WORKS4YOU AUTONOMOUS FLEET • VEO & WHISK VIDEO ENGINE • FIREBASE EDGE STREAMING", 
                  font=get_font(12, bold=True), fill=(148, 163, 184, 160))
        draw.text((width - 240, height - 48), "LATENCY: 180ms • SOC 2 AIRGAP", font=get_font(12, bold=True), fill=(56, 189, 248, 180))

        frame_path = os.path.join(temp_frames_dir, f"frame_{i:04d}.png")
        im.save(frame_path)

    out_mp4 = os.path.join(OUTPUT_DIR, "hero_ambient_stream.mp4")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-crf", "24",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for f in os.listdir(temp_frames_dir):
        os.remove(os.path.join(temp_frames_dir, f))
    os.rmdir(temp_frames_dir)
    print(f"Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")

if __name__ == "__main__":
    generate_edith_legal_reel()
    generate_4rest_reel()
    generate_founder_cashflow_reel()
    generate_hero_ambient_video()
    print("All AI video reels generated successfully!")
