from PIL import Image, ImageDraw, ImageFont
import os

public_dir = "src/frontend/public"
os.makedirs(public_dir, exist_ok=True)

size = 512
img = Image.new('RGB', (size, size), color='#2563eb')
draw = ImageDraw.Draw(img)

# Cercle blanc
draw.ellipse((100, 100, 412, 412), fill='white')

# Texte "S" au centre
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 220)
except:
    font = ImageFont.load_default()

draw.text((170, 100), "S", fill='#2563eb', font=font)

img.save(os.path.join(public_dir, "icon-512.png"))
img_192 = img.resize((192, 192))
img_192.save(os.path.join(public_dir, "icon-192.png"))
print("Icônes générées.")