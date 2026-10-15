"""Pack _build/tmp/fav-{16,32,48}.png (from render.mjs) into favicon.ico. Needs Pillow."""
import pathlib
from PIL import Image

root = pathlib.Path(__file__).resolve().parent.parent
imgs = [Image.open(root / "_build" / "tmp" / f"fav-{s}.png").convert("RGBA") for s in (16, 32, 48)]
imgs[2].save(root / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=imgs[:2])
print("wrote favicon.ico")
