# PerfectionBot/scripts/bannergenerator.py

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from collections import Counter
import os
import math
from typing import Tuple, Optional

GRADIENT_WIDTH = 1100
GRADIENT_HEIGHT = 500
DARKEN_FACTOR = 0.4
TEXT_PADDING = 28
INTERLINE_SPACING = 8
BLUR_RADIUS = 3
FONT_SIZE_SCALE = 0.06

DEFAULT_FONT_NAME = "DejaVuSans-Bold.ttf"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")
FONT_PATH = os.path.join(ASSETS_DIR, "welcomefont.otf")
RING_PATH = os.path.join(ASSETS_DIR, "ring.png")

PLACEHOLDER_COLOR = (0, 255, 38)
EXPAND_PIXELS = 5

def get_two_dominant_colors(image: Image.Image, resize: int = 100) -> Tuple[Tuple[int,int,int], Tuple[int,int,int]]:
    img = image.convert("RGB")
    small = img.resize((max(1, min(resize, img.width)), max(1, min(resize, img.height))))
    pixels = np.array(small).reshape(-1, 3)
    pixels = (pixels // 32) * 32
    counts = Counter(map(tuple, pixels))
    most_common = counts.most_common(2)
    if not most_common:
        return (128,128,128), (64,64,64)
    if len(most_common) == 1:
        return most_common[0][0], most_common[0][0]
    return most_common[0][0], most_common[1][0]

def luminance(color: Tuple[int,int,int]) -> float:
    r, g, b = color
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def darken(color: Tuple[int,int,int], factor: float) -> Tuple[int,int,int]:
    return (
        max(0, min(255, int(color[0] * factor))),
        max(0, min(255, int(color[1] * factor))),
        max(0, min(255, int(color[2] * factor)))
    )

def generate_vertical_gradient(width: int, height: int, top_color: Tuple[int,int,int], bottom_color: Tuple[int,int,int]) -> Image.Image:
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        t = y / max(1, height - 1)
        color = (
            int(top_color[0] * (1 - t) + bottom_color[0] * t),
            int(top_color[1] * (1 - t) + bottom_color[1] * t),
            int(top_color[2] * (1 - t) + bottom_color[2] * t)
        )
        gradient[y, :] = color
    return Image.fromarray(gradient)

def load_font_path_safe(path: Optional[str], size: int) -> ImageFont.FreeTypeFont:
    if path and os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            print(f"Failed to load font at {path}, using default font.")
    try:
        return ImageFont.truetype(DEFAULT_FONT_NAME, size)
    except Exception:
        print("Failed to load default font, using PIL default.")
        return ImageFont.load_default()

def compute_font_and_bbox(image: Image.Image, text: str, font_path: Optional[str] = None,
                          max_width: Optional[int] = None, max_height: Optional[int] = None,
                          start_scale: float = FONT_SIZE_SCALE):
    draw = ImageDraw.Draw(image)
    font_size = max(24, int(image.width * start_scale))
    min_font_size = 10
    if max_width is None:
        max_width = image.width - 2 * TEXT_PADDING
    if max_height is None:
        max_height = image.height - 2 * TEXT_PADDING
    font = load_font_path_safe(font_path, font_size)
    stroke_width = max(1, font_size // 24)
    while True:
        try:
            bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
        except TypeError:
            bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width <= max_width and text_height <= max_height:
            break
        if font_size <= min_font_size:
            break
        font_size -= 1
        stroke_width = max(1, font_size // 24)
        font = load_font_path_safe(font_path, font_size)
    return font, stroke_width, text_width, text_height

def draw_text_at(image: Image.Image, text: str, font: ImageFont.FreeTypeFont, stroke_width: int, x: int, y: int):
    draw = ImageDraw.Draw(image)
    base_size = getattr(font, "size", 24)
    shadow_offset = max(2, base_size // 24)
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0,0,0))
    try:
        draw.text((x, y), text, font=font, fill=(235,235,235), stroke_width=stroke_width, stroke_fill=(0,0,0))
    except TypeError:
        outline_offsets = [(-1,0),(1,0),(0,-1),(0,1)]
        for ox, oy in outline_offsets:
            draw.text((x+ox, y+oy), text, font=font, fill=(0,0,0))
        draw.text((x, y), text, font=font, fill=(235,235,235))

def cover_resize_and_crop(src_img: Image.Image, target_size: Tuple[int,int]) -> Image.Image:
    target_w, target_h = target_size
    src_w, src_h = src_img.size
    if src_w == 0 or src_h == 0:
        return Image.new("RGBA", target_size, (0,0,0,0))
    scale = max(target_w / src_w, target_h / src_h)
    new_w = max(1, int(math.ceil(src_w * scale)))
    new_h = max(1, int(math.ceil(src_h * scale)))
    resized = src_img.resize((new_w, new_h), Image.LANCZOS)
    left = max(0, (new_w - target_w) // 2)
    top = max(0, (new_h - target_h) // 2)
    right = left + target_w
    bottom = top + target_h
    return resized.crop((left, top, right, bottom))

def load_ring_safe() -> Optional[Image.Image]:
    if os.path.exists(RING_PATH):
        try:
            return Image.open(RING_PATH).convert("RGBA")
        except Exception:
            print(f"Failed to open ring image at {RING_PATH}")
            return None
    else:
        print(f"Ring image not found at {RING_PATH}")
        return None

def paste_ring_and_profile(gradient: Image.Image, profile_path: str,
    placeholder_color: Tuple[int,int,int] = PLACEHOLDER_COLOR):
    ring = load_ring_safe()
    ring_x = (gradient.width - ring.width) // 2 if ring else 0
    ring_y = (gradient.height - ring.height) // 2 if ring else 0

    if ring is None:
        try:
            src = Image.open(profile_path).convert("RGBA")
            profile_size = (200, 200)
            filled_src = cover_resize_and_crop(src, profile_size)
            profile_x = (gradient.width - profile_size[0]) // 2
            profile_y = (gradient.height - profile_size[1]) // 2
            gradient.paste(filled_src, (profile_x, profile_y), filled_src)
        except Exception as e:
            print(f"Failed to load profile image {profile_path}: {e}")
        return

    arr = np.array(ring)
    rgb_arr = arr[:, :, :3]
    match_mask = np.all(rgb_arr == np.array(placeholder_color, dtype=np.uint8), axis=2)

    if not match_mask.any():
        gradient.paste(ring, (ring_x, ring_y), ring)
        return

    ys, xs = np.where(match_mask)
    min_x = max(0, int(xs.min()) - EXPAND_PIXELS)
    max_x = min(arr.shape[1], int(xs.max()) + 1 + EXPAND_PIXELS)
    min_y = max(0, int(ys.min()) - EXPAND_PIXELS)
    max_y = min(arr.shape[0], int(ys.max()) + 1 + EXPAND_PIXELS)
    bbox_w = max_x - min_x
    bbox_h = max_y - min_y

    try:
        src = Image.open(profile_path).convert("RGBA")
    except Exception as e:
        print(f"Failed to open profile image {profile_path}: {e}")
        gradient.paste(ring, (ring_x, ring_y), ring)
        return

    filled_src = cover_resize_and_crop(src, (bbox_w, bbox_h))

    mask_full = (match_mask.astype('uint8') * 255)
    mask_img = Image.fromarray(mask_full, mode="L")
    bbox_mask = mask_img.crop((min_x, min_y, max_x, max_y))

    paste_x = ring_x + min_x
    paste_y = ring_y + min_y

    try:
        gradient.paste(filled_src, (paste_x, paste_y), bbox_mask)
    except Exception as e:
        print(f"Failed to paste profile into gradient: {e}")

    try:
        if arr.shape[2] == 4:
            alpha = arr[:, :, 3].copy()
            alpha[match_mask] = 0
            arr[:, :, 3] = alpha
        else:
            alpha = np.full((arr.shape[0], arr.shape[1]), 255, dtype=np.uint8)
            alpha[match_mask] = 0
            arr = np.dstack((arr[:, :, :3], alpha))
        ring_no_green = Image.fromarray(arr, mode="RGBA")
        gradient.paste(ring_no_green, (ring_x, ring_y), ring_no_green)
    except Exception as e:
        gradient.paste(ring, (ring_x, ring_y), ring)

def main(welcome_text: str, user_text: str, input_path: str, output_path: str):
    image = Image.open(input_path)
    c1, c2 = get_two_dominant_colors(image)
    light, dark = (c1, c2) if luminance(c1) > luminance(c2) else (c2, c1)
    light = darken(light, DARKEN_FACTOR)
    dark = darken(dark, DARKEN_FACTOR)
    gradient = generate_vertical_gradient(GRADIENT_WIDTH, GRADIENT_HEIGHT, top_color=light, bottom_color=dark)
    gradient = gradient.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS)).convert("RGBA")

    paste_ring_and_profile(gradient, input_path, placeholder_color=PLACEHOLDER_COLOR)

    user_font, user_stroke, user_w, user_h = compute_font_and_bbox(gradient, user_text, font_path=None)
    user_x = (gradient.width - user_w) // 2
    user_y = gradient.height - user_h - TEXT_PADDING - 10

    fixed_greeting_y = int(gradient.height * 0.62)
    draw = ImageDraw.Draw(gradient)
    welcome_font_size = max(24, int(gradient.width * FONT_SIZE_SCALE))
    welcome_font = load_font_path_safe(FONT_PATH if os.path.exists(FONT_PATH) else None, welcome_font_size)
    welcome_stroke = max(1, welcome_font.size // 24)
    try:
        bbox = draw.textbbox((0, 0), welcome_text, font=welcome_font, stroke_width=welcome_stroke)
    except TypeError:
        bbox = draw.textbbox((0, 0), welcome_text, font=welcome_font)
    welcome_w = bbox[2] - bbox[0]
    welcome_x = (gradient.width - welcome_w) // 2
    welcome_y = fixed_greeting_y

    draw_text_at(gradient, welcome_text, welcome_font, welcome_stroke, welcome_x, welcome_y)
    draw_text_at(gradient, user_text, user_font, user_stroke, user_x, user_y)

    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    gradient.save(output_path)

def generate_banner(w_text: str, user_name: str, input_image_path: str, output_image_path: str):
    main(w_text, user_name, input_image_path, output_image_path)