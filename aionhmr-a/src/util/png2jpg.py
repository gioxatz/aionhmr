from PIL import Image
import sys
import os

input_path = sys.argv[1]
output_path = os.path.splitext(input_path)[0] + ".jpg"

try:
    img = Image.open(input_path)

    # Handle transparency (PNG → JPG)
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")

    img.save(output_path, "JPEG", quality=95)

    # Remove original PNG
    os.remove(input_path)

    print(f"Converted: {input_path} -> {output_path}")

except Exception as e:
    print(f"Error converting {input_path}: {e}")
    sys.exit(1)