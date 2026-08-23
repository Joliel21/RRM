from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'public/images/community-gallery'
OUT = ROOT / 'public/images/rare-pages'
W, H = 480, 681
BG = '#073341'
DEEP = '#052833'
TEAL = '#0f7f86'
CYAN = '#43c6d6'
WHITE = '#ffffff'
CREAM = '#e8e4dc'
MUTED = '#a9d7dc'

files = sorted(
    [p for p in SRC.iterdir() if p.is_file() and p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}],
    key=lambda p: p.name.lower(),
)

# Requested swap: the wide group photograph becomes the page-90 hero, while
# the table-display photograph takes the group's former page-91 position.
table_photo = next(p for p in files if p.name == '20191112_16025610-768x1024.jpg')
group_photo = next(p for p in files if p.name == 'Community_Group-1024x498.jpeg')
table_index = files.index(table_photo)
group_index = files.index(group_photo)
files[table_index], files[group_index] = files[group_index], files[table_index]

font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_reg = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_serif = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

def font(path, size):
    return ImageFont.truetype(path, size)


def textured_bg():
    """Create a subtle editorial teal paper texture."""
    canvas = Image.new('RGB', (W, H), BG)
    px = canvas.load()
    rng = random.Random(9307)
    base = (7, 51, 65)
    for y in range(H):
        for x in range(W):
            grain = rng.choice((-2, -1, 0, 0, 0, 1, 2))
            px[x, y] = tuple(max(0, min(255, c + grain)) for c in base)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(-H, W, 22):
        od.line((x, 0, x + H, H), fill=(67, 198, 214, 10), width=1)
    for y in range(18, H, 34):
        od.line((0, y, W, y), fill=(255, 255, 255, 5), width=1)
    return Image.alpha_composite(canvas.convert('RGBA'), overlay).convert('RGB')

def rounded_card(canvas, box, radius=8, shadow=True):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(canvas)
    if shadow:
        d.rounded_rectangle((x0 + 2, y0 + 3, x1 + 2, y1 + 3), radius=radius, fill=DEEP)
    d.rounded_rectangle(box, radius=radius, fill=WHITE, outline='#d8d1c5', width=1)

def paste_contain(canvas, src_path, box, pad=0):
    """Fit the complete image and make the frame follow the actual image bounds."""
    x0, y0, x1, y1 = box
    aw, ah = x1 - x0, y1 - y0
    with Image.open(src_path) as im:
        im = im.convert('RGB')
        fitted = ImageOps.contain(im, (aw, ah), Image.Resampling.LANCZOS)
    px = x0 + (aw - fitted.width) // 2
    py = y0 + (ah - fitted.height) // 2
    actual = (px, py, px + fitted.width, py + fitted.height)
    d = ImageDraw.Draw(canvas)
    # Tight shadow and border: no oversized cream box behind the photograph.
    d.rounded_rectangle((actual[0] + 2, actual[1] + 3, actual[2] + 2, actual[3] + 3),
                        radius=5, fill=DEEP)
    canvas.paste(fitted, (px, py))
    d.rounded_rectangle(actual, radius=4, outline=WHITE, width=3)


def footer(canvas, page_no):
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, H - 12, W, H), fill=DEEP)
    d.text((18, H - 29), 'RARE COMMUNITY', font=font(font_bold, 8), fill=CYAN)
    num = str(page_no)
    bbox = d.textbbox((0, 0), num, font=font(font_bold, 9))
    d.text((W - 18 - (bbox[2] - bbox[0]), H - 29), num, font=font(font_bold, 9), fill=WHITE)

def section_header(canvas, title, kicker='COMMUNITY GALLERY'):
    d = ImageDraw.Draw(canvas)
    # Slim editorial rule rather than a heavy boxed banner.
    d.rectangle((24, 27, 104, 30), fill=CYAN)
    d.text((24, 39), kicker, font=font(font_bold, 8), fill=MUTED)
    d.text((24, 55), title, font=font(font_serif, 22), fill=WHITE)
    d.line((24, 87, 456, 87), fill=TEAL, width=1)

# Page 90: editorial opener plus seven images.
p = textured_bg()
d = ImageDraw.Draw(p)
d.rectangle((0, 0, W, 14), fill=DEEP)
d.text((28, 40), 'RARE COMMUNITY', font=font(font_bold, 9), fill=MUTED)
d.rectangle((28, 57, 132, 60), fill=CYAN)
d.text((28, 72), 'Community', font=font(font_serif, 39), fill=WHITE)
d.text((28, 113), 'Gallery', font=font(font_serif, 39), fill=WHITE)
d.multiline_text(
    (30, 163),
    'A visual celebration of the people,\nfamilies, advocates and organisations\nshaping the rare disease community.',
    font=font(font_reg, 13),
    fill=WHITE,
    spacing=5,
)
paste_contain(p, files[0], (18, 226, 462, 432))
small = files[1:7]
coords = []
for r in range(2):
    for c in range(3):
        x = 18 + c * 151
        y = 444 + r * 101
        coords.append((x, y, x + 142, y + 92))
for f, b in zip(small, coords):
    paste_contain(p, f, b)
footer(p, 90)
p.save(OUT / 'community-gallery-page-90.png', quality=95)

# Pages 91-93: clean editorial headings and twelve uncropped images per page.
remaining = files[7:]
titles = {
    91: 'A Community in Motion',
    92: 'Faces of the Community',
    93: 'Together, We Are Rare',
}
for page_no, chunk_start in zip((91, 92, 93), (0, 12, 24)):
    chunk = remaining[chunk_start:chunk_start + 12]
    p = textured_bg()
    d = ImageDraw.Draw(p)
    d.rectangle((0, 0, W, 14), fill=DEEP)
    section_header(p, titles[page_no])
    top = 96
    left = 16
    gapx = 6
    gapy = 6
    cw = 145
    ch = 132
    for i, f in enumerate(chunk):
        r = i // 3
        c = i % 3
        x = left + c * (cw + gapx)
        y = top + r * (ch + gapy)
        paste_contain(p, f, (x, y, x + cw, y + ch))
    footer(p, page_no)
    p.save(OUT / f'community-gallery-page-{page_no}.png', quality=95)

print(f'Built 4 pages from {len(files)} images')
