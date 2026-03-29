"""DINOv2 Demo — See how visual similarity works on engineering drawings.

Run: python demos/dinov2_demo.py

What it does:
  1. Loads DINOv2 (Meta's vision model)
  2. Creates sample "drawings" (simple shapes)
  3. Computes fingerprints (768-dim vectors)
  4. Shows which shapes are most similar to each other

Requirements: pip install torch torchvision  (~1.5GB download)
RAM needed: ~4GB. Close Chrome/other apps before running.
"""
import sys
import time
import numpy as np
from PIL import Image, ImageDraw

# ── Step 0: Check if torch is installed ──────────────────────
try:
    import torch
    from torchvision import transforms
    print(f"PyTorch {torch.__version__} found")
except ImportError:
    print("PyTorch not installed. Run:")
    print("  pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
    print("\nThis downloads ~1.5GB. On 8GB RAM, use CPU-only (above command).")
    sys.exit(1)


# ── Step 1: Create fake "engineering drawings" ───────────────
def make_cylinder(size=224):
    """Simulate a turned cylindrical part drawing."""
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    # Main body (rectangle = side view of cylinder)
    draw.rectangle([40, 60, 184, 164], outline="black", width=2)
    # Center line
    draw.line([112, 40, 112, 184], fill="gray", width=1)
    # Dimension lines
    draw.line([40, 180, 184, 180], fill="blue", width=1)
    draw.text((90, 182), "120mm", fill="blue")
    return img

def make_cylinder_similar(size=224):
    """Slightly different cylinder — should score HIGH similarity."""
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([35, 55, 189, 169], outline="black", width=2)
    draw.line([112, 35, 112, 189], fill="gray", width=1)
    draw.line([35, 185, 189, 185], fill="blue", width=1)
    draw.text((85, 187), "130mm", fill="blue")
    return img

def make_lbracket(size=224):
    """L-bracket — should score LOW similarity to cylinders."""
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    # L-shape
    draw.polygon([40, 40, 100, 40, 100, 100, 184, 100, 184, 160, 40, 160],
                 outline="black", width=2)
    draw.text((50, 170), "L-Bracket", fill="black")
    return img

def make_gear(size=224):
    """Gear profile — complex shape."""
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    # Outer circle
    draw.ellipse([30, 30, 194, 194], outline="black", width=2)
    # Inner circle (bore)
    draw.ellipse([80, 80, 144, 144], outline="black", width=2)
    # Teeth (simplified as lines)
    import math
    cx, cy, r = 112, 112, 82
    for i in range(12):
        angle = math.radians(i * 30)
        x1 = cx + r * math.cos(angle)
        y1 = cy + r * math.sin(angle)
        x2 = cx + (r + 15) * math.cos(angle)
        y2 = cy + (r + 15) * math.sin(angle)
        draw.line([x1, y1, x2, y2], fill="black", width=2)
    return img


# ── Step 2: Load DINOv2 ─────────────────────────────────────
print("\nLoading DINOv2 model (first time downloads ~350MB)...")
t0 = time.time()

model = torch.hub.load("facebookresearch/dinov2", "dinov2_vits14", pretrained=True)
model.eval()

load_time = time.time() - t0
print(f"Model loaded in {load_time:.1f}s")
print(f"RAM used by model: ~{torch.cuda.memory_allocated()/1e6:.0f}MB (GPU)" if torch.cuda.is_available() else "Running on CPU")

# DINOv2 preprocessing
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


# ── Step 3: Compute embeddings ───────────────────────────────
def get_embedding(img: Image.Image) -> np.ndarray:
    tensor = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        features = model(tensor)
    vec = features[0].numpy()
    vec = vec / np.linalg.norm(vec)  # L2 normalize
    return vec


print("\nComputing embeddings for 4 drawings...")
drawings = {
    "Cylinder A (120mm)": make_cylinder(),
    "Cylinder B (130mm)": make_cylinder_similar(),
    "L-Bracket":          make_lbracket(),
    "Gear":               make_gear(),
}

embeddings = {}
for name, img in drawings.items():
    t0 = time.time()
    embeddings[name] = get_embedding(img)
    elapsed = time.time() - t0
    print(f"  {name}: {embeddings[name].shape[0]}-dim vector ({elapsed:.2f}s)")


# ── Step 4: Compare all pairs ────────────────────────────────
print("\n" + "=" * 60)
print("SIMILARITY MATRIX (cosine similarity, 0-1)")
print("=" * 60)

names = list(drawings.keys())
print(f"\n{'':30s}", end="")
for n in names:
    print(f"{n[:12]:>14s}", end="")
print()

for i, name_a in enumerate(names):
    print(f"{name_a:30s}", end="")
    for j, name_b in enumerate(names):
        sim = float(np.dot(embeddings[name_a], embeddings[name_b]))
        sim = max(0.0, min(1.0, sim))
        if i == j:
            marker = "  ---"
            print(f"{'---':>14s}", end="")
        else:
            pct = f"{sim:.1%}"
            print(f"{pct:>14s}", end="")
    print()


# ── Step 5: Show the key insight ─────────────────────────────
sim_cylinders = float(np.dot(embeddings["Cylinder A (120mm)"], embeddings["Cylinder B (130mm)"]))
sim_cyl_bracket = float(np.dot(embeddings["Cylinder A (120mm)"], embeddings["L-Bracket"]))
sim_cyl_gear = float(np.dot(embeddings["Cylinder A (120mm)"], embeddings["Gear"]))

print(f"""
KEY INSIGHT:
  Cylinder A vs Cylinder B: {sim_cylinders:.1%}  <-- HIGH (similar shapes!)
  Cylinder A vs L-Bracket:  {sim_cyl_bracket:.1%}  <-- LOW (different shapes)
  Cylinder A vs Gear:       {sim_cyl_gear:.1%}  <-- LOW (different shapes)

This is how similarity search works:
  1. Upload a new drawing
  2. DINOv2 converts it to a {embeddings[names[0]].shape[0]}-number fingerprint
  3. Compare fingerprint against all stored drawings
  4. Return the most similar ones (highest score)

On your system: We use Gemini API instead (same idea, zero RAM).
DINOv2 is the upgrade path when you have a server with more RAM.
""")

# Save sample images so user can see them
output_dir = "demos/sample_drawings"
import os
os.makedirs(output_dir, exist_ok=True)
for name, img in drawings.items():
    safe_name = name.replace(" ", "_").replace("(", "").replace(")", "").lower()
    img.save(f"{output_dir}/{safe_name}.png")
print(f"Sample drawings saved to {output_dir}/")
