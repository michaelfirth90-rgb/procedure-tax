#!/usr/bin/env python3
"""
sweep-icon.py — repaint the procedure.tax mark in the site's own title sweep.

brand-sweep.css paints the masthead and every page title with

    --title-sweep: linear-gradient(90deg, #0A2E6E 0%, #1F712F 100%)

and it paints it FLAT, through a glyph mask, via background-clip: text. There is
no shading inside a swept title, just the gradient cut to the shape of the
letters. This does the same to the mark: build a mask from the artwork, paint
that gradient through it, composite over white.

Two earlier attempts, both wrong, both worth recording:

  1. Keep the artwork's shading and move only its hue. The mark's shading is a
     BEVEL — light along the top-left of every stroke, dark along the bottom-
     right. A bevel running diagonally underneath a gradient running horizontally
     does not read as a sweep, it reads as blotches. Measured, the column means
     wandered a whole step off the ramp at the green end.

  2. Pure flat fill through one mask. Smooth, and it destroys the mark. The
     green arc sits DIRECTLY on the T's crossbar with no gap between them — in
     the original they are told apart by colour alone, arc green against bar
     teal. Give both the same gradient and they weld into one heavy blob across
     the top-left, and the mark stops reading as a C and a T.

What works is flat plus a HIGH-PASS of the original's luminance. The blotches in
(1) were low-frequency: the broad bevel. The structure lost in (2) was high-
frequency: the boundaries where one stroke crosses another. Blurring the
original's luminance and subtracting gives exactly the second without the first,
so the gradient stays smooth across x while every internal edge survives.

Measured on the result, column mean against the ramp:

    25%  #134060  vs  #0F3F5E      75%  #1B5F3F  vs  #1A603F
    50%  #215C5B  vs  #14504E     100%  #276D33  vs  #1F712F

MASK. The files are opaque RGB on white with no alpha, so the shape has to be
recovered. Saturation separates it cleanly — measured on logo.png:

    saturation   px     mean luminance   what it is
    0.02-0.12    2894      0.96-0.98     pale interior wash, and the halo
    0.12-0.20     592      0.66          the anti-aliased edge band
    0.20-0.35    3464      0.52          the teal strokes
    0.35-0.60     516      0.71          the light green top arc

so a smoothstep from 0.06 to 0.20 takes both inks at full strength, takes the
edge band as partial coverage, and leaves the wash at nothing. Luminance would
NOT separate it: the green arc sits at 0.71 and the wash at 0.96, far too close,
which is why the arc survives here and would have been eaten by a threshold on
darkness.

The gradient is hung on the mask's bounding box, not on the canvas, so the ends
land on exactly #0A2E6E and #1F712F however much white padding a file has around
the mark — and the three files have very different amounts.

    python3 sweep-icon.py logo.png.orig logo.png
"""

import sys
import numpy as np
from PIL import Image, ImageFilter

SWEEP_A = (0x0A, 0x2E, 0x6E)    # navy,  left  end
SWEEP_B = (0x1F, 0x71, 0x2F)    # green, right end

MASK_LO, MASK_HI = 0.06, 0.20   # saturation band for the coverage mask
DETAIL = 1.15                   # how hard the internal edges come back
BG = (255, 255, 255)


def _to_linear(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _to_srgb(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def _blur(arr, sigma):
    im = Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(sigma))).astype(float) / 255


def sweep(img, detail=DETAIL):
    a = np.asarray(img.convert("RGB")).astype(np.float64) / 255.0
    h, w, _ = a.shape

    # ---- coverage mask ----
    sat = a.max(2) - a.min(2)
    t = np.clip((sat - MASK_LO) / (MASK_HI - MASK_LO), 0.0, 1.0)
    cov = t * t * (3 - 2 * t)                      # smoothstep
    if cov.max() <= 0:
        return img.convert("RGB")

    cols = np.where(cov.max(0) > 0.5)[0]
    if len(cols) == 0:
        cols = np.where(cov.max(0) > 0)[0]
    x0, x1 = int(cols[0]), int(cols[-1])

    # ---- the ramp ----
    # CSS interpolates a gradient in sRGB, so this does too. The point is to
    # match the title sitting next to it, not to be prettier than it.
    u = np.clip((np.arange(w) - x0) / max(1, x1 - x0), 0.0, 1.0)
    A = np.array(SWEEP_A, dtype=np.float64) / 255.0
    B = np.array(SWEEP_B, dtype=np.float64) / 255.0
    grad = np.broadcast_to(
        (A[None, :] + (B - A)[None, :] * u[:, None])[None, :, :], (h, w, 3))

    # ---- high-pass of the original's luminance ----
    # Masked blur: blur L*cov and cov separately and divide, so the white
    # outside the mark cannot bleed in and leave a bright halo along every
    # outer edge. sigma scales with the file so the 16px favicon frame and the
    # 246px logo keep the same detail at their own scale.
    L = a @ [0.2126, 0.7152, 0.0722]
    sigma = max(0.8, w / 120.0)
    num = _blur(L * cov, sigma)
    den = _blur(cov, sigma)
    L_blur = np.where(den > 0.02, num / np.maximum(den, 1e-6), L)
    out = np.clip(grad + ((L - L_blur) * detail)[..., None], 0.0, 1.0)

    # Composite in LINEAR light. Compositing anti-aliased edges in gamma space
    # is the classic way to get a dark rim around artwork; at 16px, where a
    # third of the mark is edge pixels, it is plainly visible.
    bg = _to_linear(np.array(BG, dtype=np.float64) / 255.0)[None, None, :]
    al = cov[..., None]
    px = _to_srgb(_to_linear(out) * al + bg * (1 - al))
    return Image.fromarray(np.rint(px * 255).astype(np.uint8), "RGB")


def main(src, dst):
    if src.lower().endswith(".ico"):
        im = Image.open(src)
        sizes = sorted(im.info.get("sizes") or {im.size})
        frames = []
        for s in sizes:
            im.size = s          # selects the stored frame; not a resize
            frames.append(sweep(im.copy()))
        # Each frame is recoloured from its own hand-hinted artwork, and
        # append_images keeps them — otherwise Pillow resamples the 64 down to
        # 16 and the hinting is gone.
        frames[-1].save(dst, format="ICO", sizes=sizes, append_images=frames[:-1])
        print(f"{dst}: {len(sizes)} frames {sizes}")
    else:
        sweep(Image.open(src)).save(dst)
        print(f"{dst}: {Image.open(dst).size}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
