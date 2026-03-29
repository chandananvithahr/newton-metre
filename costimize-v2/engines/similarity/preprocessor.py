"""Drawing preprocessor — converts any input format to clean image for DINOv2.

Handles: PDF, PNG, JPG, JPEG, DXF (rendered via ezdxf+matplotlib).
Output: clean 224×224 image (PIL.Image) + 300px thumbnail.

Image processing pipeline:
  1. Decode input bytes → PIL Image
  2. Convert to grayscale → enhance contrast
  3. Resize to 224×224 (DINOv2 input size)
  4. Generate 300px thumbnail for UI display
"""
import io
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps


# DINOv2 expects 224×224 input
EMBED_SIZE = (224, 224)
THUMBNAIL_SIZE = (300, 300)


def preprocess_drawing(
    file_bytes: bytes,
    filename: str,
) -> tuple[Image.Image, Image.Image]:
    """Convert drawing file to clean image + thumbnail.

    Args:
        file_bytes: Raw file bytes
        filename: Original filename (used to detect format)

    Returns:
        (embed_image, thumbnail) — both PIL Images.
        embed_image is 224×224 RGB for DINOv2.
        thumbnail is 300×300 for UI display.

    Raises:
        ValueError: If file format is unsupported
    """
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        image = _pdf_to_image(file_bytes)
    elif ext == ".dxf":
        image = _dxf_to_image(file_bytes)
    elif ext in (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"):
        image = Image.open(io.BytesIO(file_bytes))
    else:
        raise ValueError(f"Unsupported file format: {ext}. Use PDF, PNG, JPG, or DXF.")

    # Convert to RGB (DINOv2 expects 3 channels)
    image = image.convert("RGB")

    # Enhance for engineering drawings (high contrast, clean lines)
    image = _enhance_drawing(image)

    # Generate both sizes
    embed_image = image.copy()
    embed_image = ImageOps.fit(embed_image, EMBED_SIZE, method=Image.LANCZOS)

    thumbnail = image.copy()
    thumbnail.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)

    return embed_image, thumbnail


def _enhance_drawing(image: Image.Image) -> Image.Image:
    """Enhance engineering drawing for better feature extraction.

    Engineering drawings are typically:
    - High contrast (black lines on white background)
    - May be scanned (slightly rotated, noisy)
    - Have dimension lines, annotations, title blocks

    We enhance contrast and sharpness to make features more distinct.
    """
    # Boost contrast (makes lines crisper)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    # Boost sharpness (makes fine details clearer)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.3)

    return image


def _pdf_to_image(file_bytes: bytes) -> Image.Image:
    """Convert first page of PDF to image.

    Uses pdf2image (poppler) if available, falls back to PyMuPDF (fitz).
    """
    try:
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(file_bytes, first_page=1, last_page=1, dpi=200)
        return images[0]
    except ImportError:
        pass

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page = doc[0]
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        return Image.open(io.BytesIO(img_bytes))
    except ImportError:
        pass

    raise ImportError(
        "PDF support requires pdf2image (poppler) or PyMuPDF. "
        "Install: pip install pdf2image  OR  pip install PyMuPDF"
    )


def _dxf_to_image(file_bytes: bytes) -> Image.Image:
    """Render DXF file to image using ezdxf + matplotlib."""
    try:
        import ezdxf
        from ezdxf.addons.drawing import matplotlib as ezdxf_matplotlib
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        doc = ezdxf.read(io.BytesIO(file_bytes))
        msp = doc.modelspace()

        fig = plt.figure(figsize=(8, 8), dpi=200)
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = ezdxf_matplotlib.MatplotlibBackend(ax)

        from ezdxf.addons.drawing import Frontend
        Frontend(ctx, doc).draw_layout(msp)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)
    except ImportError:
        raise ImportError(
            "DXF support requires ezdxf and matplotlib. "
            "Install: pip install ezdxf matplotlib"
        )


def save_thumbnail(thumbnail: Image.Image, drawing_id: str, output_dir: Path) -> Path:
    """Save thumbnail to disk and return path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{drawing_id}.png"
    thumbnail.save(path, "PNG")
    return path
