from PIL import Image, ImageDraw, ImageFont
import math

WIDTH = 1200
HEIGHT = 630
OUTPUT_PATH = "/Users/robert/source/agent365-resources/images/og-image.png"

BG_COLOR = (15, 27, 45)          # #0f1b2d
ACCENT_BLUE = (0, 120, 212)       # #0078d4
ACCENT_BLUE_DIM = (0, 80, 140)    # darker blue for subtle shapes
WHITE = (255, 255, 255)
GRID_COLOR = (0, 120, 212, 18)    # very faint blue grid lines

img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR + (255,))
draw = ImageDraw.Draw(img)


# --- Decorative background: subtle dot grid ---
grid_spacing = 48
for x in range(0, WIDTH + grid_spacing, grid_spacing):
    for y in range(0, HEIGHT + grid_spacing, grid_spacing):
        r = 1
        draw.ellipse(
            [(x - r, y - r), (x + r, y + r)],
            fill=(0, 120, 212, 22),
        )

# --- Decorative: large faint circle (top-right) ---
cx, cy = WIDTH - 80, -60
for ring in range(3):
    radius = 260 + ring * 80
    alpha = 30 - ring * 8
    draw.ellipse(
        [(cx - radius, cy - radius), (cx + radius, cy + radius)],
        outline=(0, 120, 212, alpha),
        width=1,
    )

# --- Decorative: smaller circle (bottom-left) ---
cx2, cy2 = 100, HEIGHT + 40
for ring in range(2):
    radius = 180 + ring * 70
    alpha = 20 - ring * 6
    draw.ellipse(
        [(cx2 - radius, cy2 - radius), (cx2 + radius, cy2 + radius)],
        outline=(0, 120, 212, alpha),
        width=1,
    )

# --- Decorative: diagonal accent lines (bottom-right) ---
for i in range(6):
    offset = i * 22
    x_start = WIDTH - 320 + offset
    x_end = WIDTH - 60 + offset
    y_start = HEIGHT - 40
    y_end = HEIGHT + 80
    alpha = 35 - i * 5
    draw.line(
        [(x_start, y_start), (x_end, y_end)],
        fill=(0, 120, 212, alpha),
        width=1,
    )

# --- Accent bar (left edge) ---
draw.rectangle([(0, 0), (5, HEIGHT)], fill=ACCENT_BLUE + (255,))

# --- Accent horizontal rule under title area ---
rule_y = 370
draw.rectangle(
    [(120, rule_y), (1080, rule_y + 2)],
    fill=(0, 120, 212, 100),
)

# --- Font loading: try common system fonts, fall back to default ---
def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates_bold = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]
    candidates_regular = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    paths = candidates_bold if bold else candidates_regular
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


font_title = load_font(68, bold=True)
font_subtitle = load_font(36, bold=False)

TITLE_TEXT = "Microsoft Agent 365 Resources"
SUBTITLE_TEXT = "https://aka.ms/agent365/resources"

# --- Draw title (centered, white) ---
title_bbox = draw.textbbox((0, 0), TITLE_TEXT, font=font_title)
title_w = title_bbox[2] - title_bbox[0]
title_h = title_bbox[3] - title_bbox[1]
title_x = (WIDTH - title_w) // 2
title_y = 230

draw.text((title_x, title_y), TITLE_TEXT, font=font_title, fill=WHITE)

# --- Draw subtitle (centered, Microsoft blue) ---
sub_bbox = draw.textbbox((0, 0), SUBTITLE_TEXT, font=font_subtitle)
sub_w = sub_bbox[2] - sub_bbox[0]
sub_x = (WIDTH - sub_w) // 2
sub_y = title_y + title_h + 28

draw.text((sub_x, sub_y), SUBTITLE_TEXT, font=font_subtitle, fill=WHITE)

# --- Convert RGBA -> RGB before saving as PNG (keeps transparency support) ---
final = img.convert("RGB")
final.save(OUTPUT_PATH, "PNG", optimize=False)
print(f"Saved: {OUTPUT_PATH}")
print(f"Size: {final.size}")
