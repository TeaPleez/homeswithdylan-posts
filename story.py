#!/usr/bin/env python3
"""Turn approved open house carousel slides into 1080x1920 Instagram story frames.

Usage:
  python3 story.py --slides DIR --out DIR --variant thu|sat --sat-date "Nov 21" \
      [--days both|sat|sun] [--fonts DIR]

DIR must hold slide-01.jpg (the carousel cover) ... slide-NN.jpg (one per listing),
any size with a 4:5 shape. Output: story-01.jpg (new 9:16 cover) + story-02.jpg ...
(each listing slide centred on the brand navy, with a small label underneath).
--days says which days have open houses (from the caption's SATURDAY / SUNDAY lines).
"""
import argparse, glob, os, sys
from datetime import date, datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
NAVY = (22, 50, 61)
ACCENT = (191, 112, 56)
GOLD = (214, 160, 100)
CREAM = (246, 241, 232)
MUTED = (120, 140, 150)

FONT_DIRS = ["/usr/share/fonts/truetype/google-fonts", "/usr/share/fonts/truetype/google-fonts/ofl/dmsans",
             "/Library/Fonts", os.path.expanduser("~/Library/Fonts")]


def find_font(names, extra):
    dirs = ([extra] if extra else []) + FONT_DIRS + [os.path.dirname(os.path.abspath(__file__))]
    for d in dirs:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None


def font(path, size, weight=None):
    if not path:
        return ImageFont.load_default(size)
    f = ImageFont.truetype(path, size)
    if weight:
        try:
            f.set_variation_by_name(weight)
        except Exception:
            try:
                axes = f.get_variation_axes()
                f.set_variation_by_axes([{"wght": 600}.get(a.get("name", b"").decode() if isinstance(a.get("name"), bytes) else a.get("name"), a["default"]) for a in axes])
            except Exception:
                pass
    return f


def wrap(draw, text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slides", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--variant", choices=["thu", "sat"], required=True)
    ap.add_argument("--sat-date", required=True, help='Saturday as "Mon D", e.g. "Nov 21"')
    ap.add_argument("--days", choices=["both", "sat", "sun"], default="both")
    ap.add_argument("--year", type=int, default=date.today().year)
    ap.add_argument("--fonts", default=None)
    a = ap.parse_args()

    slides = sorted(glob.glob(os.path.join(a.slides, "slide-*.jpg")))
    if len(slides) < 2:
        sys.exit("need slide-01.jpg (cover) plus at least one listing slide")
    listings = slides[1:]
    if len(listings) > 9:
        sys.exit("a story upload takes at most 10 images (cover + 9 listings)")
    os.makedirs(a.out, exist_ok=True)

    serif = find_font(["Lora-Variable.ttf", "Lora[wght].ttf", "Lora-SemiBold.ttf"], a.fonts)
    sans = find_font(["DMSans[opsz,wght].ttf", "DMSans-Regular.ttf"], a.fonts)

    sat = datetime.strptime(f"{a.sat_date} {a.year}", "%b %d %Y").date()
    sun = sat + timedelta(days=1)
    fmt = lambda d: d.strftime("%A, %b ") + str(d.day)
    if a.days == "both":
        dates = f"{fmt(sat)} & {fmt(sun)}"
    else:
        dates = fmt(sat if a.days == "sat" else sun)

    if a.variant == "thu":
        headline = "This weekend in Victoria" if a.days == "both" else f"This {'Saturday' if a.days == 'sat' else 'Sunday'} in Victoria"
        label = "OPEN HOUSES THIS WEEKEND"
    else:  # posted Saturday morning
        headline = {"both": "Today & tomorrow in Victoria", "sat": "Today in Victoria", "sun": "Tomorrow in Victoria"}[a.days]
        label = {"both": "OPEN HOUSES TODAY & TOMORROW", "sat": "OPEN HOUSES TODAY", "sun": "OPEN HOUSES TOMORROW"}[a.days]
    n = len(listings)
    homes = f"{n} home{'s' if n != 1 else ''} to tour"

    # ---- cover frame (same look as the carousel cover, stretched to 9:16)
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    x = 100
    f_kick = font(sans, 40, "Regular")
    f_head = font(serif, 128, "SemiBold")
    f_sub = font(sans, 44, "Regular")
    f_homes = font(sans, 44, "Medium")
    f_foot = font(sans, 30, "Regular")
    head_lines = wrap(d, headline, f_head, W - 2 * x)
    block_h = 6 + 70 + 70 + len(head_lines) * 140 + 30 + 60 + 50 + 60
    y = (H - block_h) // 2 - 40
    d.rectangle([x, y, x + 100, y + 5], fill=ACCENT)
    y += 6 + 50
    d.text((x, y), "OPEN HOUSES", font=f_kick, fill=GOLD)
    y += 90
    for ln in head_lines:
        d.text((x, y), ln, font=f_head, fill=CREAM)
        y += 140
    y += 45
    for ln in wrap(d, dates, f_sub, W - 2 * x):
        d.text((x, y), ln, font=f_sub, fill=CREAM)
        y += 60
    y += 40
    d.text((x, y), homes, font=f_homes, fill=GOLD)
    d.text((x, H - 330), "Tap through for each home →", font=f_foot, fill=MUTED)
    d.text((x, H - 280), "@homeswithdylan", font=f_foot, fill=MUTED)
    rt = "eXp Realty"
    d.text((W - x - d.textlength(rt, font=f_foot), H - 280), rt, font=f_foot, fill=MUTED)
    im.save(os.path.join(a.out, "story-01.jpg"), quality=92, optimize=True)

    # ---- one frame per listing: the approved slide, centred, with a small label below
    f_lab = font(sans, 34, "Medium")
    sw, sh = W, int(W * 5 / 4)  # 1080 x 1350
    top = (H - sh) // 2
    for i, p in enumerate(listings, start=2):
        src = Image.open(p).convert("RGB").resize((sw, sh), Image.LANCZOS)
        im = Image.new("RGB", (W, H), NAVY)
        im.paste(src, (0, top))
        d = ImageDraw.Draw(im)
        lw = d.textlength(label, font=f_lab)
        d.text(((W - lw) / 2, top + sh + 55), label, font=f_lab, fill=GOLD)
        im.save(os.path.join(a.out, f"story-{i:02d}.jpg"), quality=92, optimize=True)
    print(f"wrote {n + 1} frames to {a.out}")


if __name__ == "__main__":
    main()
