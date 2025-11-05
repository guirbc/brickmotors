# market/utils/images.py
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from PIL import Image

# market/utils/images.py
from typing import Any, cast
from PIL import Image

# Pylance às vezes não conhece .Resampling/.LANCZOS/.BICUBIC
# Pegamos de forma dinâmica, com fallback.
_Img = cast(Any, Image)                           # ajuda o type-checker
_Resampling = getattr(_Img, "Resampling", _Img)   # Pillow>=10 usa Image.Resampling

_LANCZOS = getattr(_Resampling, "LANCZOS",
           getattr(_Img, "LANCZOS", None))        # Pillow<10
_BICUBIC = getattr(_Resampling, "BICUBIC",
           getattr(_Img, "BICUBIC", 3))           # valor padrão 3

RESAMPLE = _LANCZOS or _BICUBIC                   # use LANCZOS se houver, senão BICUBIC

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_MB = 10
MIN_WIDTH, MIN_HEIGHT = 800, 600


def validate_image(uploaded_file):
    if uploaded_file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValidationError("Formato não suportado. Use JPEG, PNG ou WebP.")
    if uploaded_file.size > MAX_FILE_MB * 1024 * 1024:
        raise ValidationError(f"Arquivo muito grande (máx {MAX_FILE_MB}MB).")

    uploaded_file.seek(0)
    im = Image.open(uploaded_file)
    w, h = im.size
    if w < MIN_WIDTH or h < MIN_HEIGHT:
        raise ValidationError(f"Imagem muito pequena (mín {MIN_WIDTH}x{MIN_HEIGHT}).")
    uploaded_file.seek(0)


def _open_and_fix(fileobj):
    im = Image.open(fileobj)
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    return im


def _save(img, fmt="JPEG", quality=85):
    buf = BytesIO()
    params = dict(format=fmt, quality=quality, optimize=True)
    if fmt == "WEBP":
        params["quality"] = 80
    img.save(buf, **params)
    return ContentFile(buf.getvalue())


def resize_max(img, mw, mh):
    im = img.copy()
    im.thumbnail((mw, mh), RESAMPLE)
    return im


def cover_crop(img, w, h):
    im = img.copy()
    W, H = im.size
    tr, cr = w / h, W / H
    if cr > tr:
        new_w = int(H * tr)
        x = (W - new_w) // 2
        im = im.crop((x, 0, x + new_w, H))
    else:
        new_h = int(W / tr)
        y = (H - new_h) // 2
        im = im.crop((0, y, W, y + new_h))
    return im.resize((w, h), RESAMPLE)


def make_variants(fileobj):
    base = _open_and_fix(fileobj)
    original = resize_max(base, 2000, 2000)
    card = cover_crop(base, 800, 600)
    thumb = cover_crop(base, 400, 300)
    return {
        "original": _save(original, "JPEG", 85),
        "card": _save(card, "JPEG", 85),
        "thumb": _save(thumb, "JPEG", 85),
    }
