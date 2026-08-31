#!/usr/bin/env python3
"""Icônes d'écran d'accueil. Remplace par le vrai logo quand tu l'as."""
import json, pathlib
from PIL import Image, ImageDraw, ImageFont

cfg = json.loads(pathlib.Path("config.json").read_text(encoding="utf-8"))
monogramme = (cfg["prenom"][:1] + cfg["nom"][:1]).upper()

FONTES = ["/System/Library/Fonts/SFNSRounded.ttf",
          "/System/Library/Fonts/SFNS.ttf",
          "/System/Library/Fonts/Helvetica.ttc"]

def fonte(taille):
    for f in FONTES:
        if pathlib.Path(f).exists():
            try: return ImageFont.truetype(f, taille)
            except OSError: continue
    return ImageFont.load_default()

for taille in (180, 512):
    img = Image.new("RGB", (taille, taille), "#141418")
    d = ImageDraw.Draw(img)
    # léger dégradé vertical pour éviter l'aplat mort
    for y in range(taille):
        t = y / taille
        d.line([(0, y), (taille, y)],
               fill=(int(30 - 8*t), int(30 - 8*t), int(36 - 8*t)))
    f = fonte(int(taille * 0.42))
    b = d.textbbox((0, 0), monogramme, font=f)
    d.text(((taille - (b[2]-b[0]))/2 - b[0], (taille - (b[3]-b[1]))/2 - b[1]),
           monogramme, font=f, fill="#f4f4f6")
    img.save(f"icon-{taille}.png")
    print(f"✓ icon-{taille}.png ({monogramme})")
