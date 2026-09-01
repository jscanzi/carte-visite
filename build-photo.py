#!/usr/bin/env python3
"""Prépare la photo du recto.

Le recadrage est celui du fill Figma, appliqué UNE FOIS ici plutôt qu'à
l'exécution : le navigateur n'a plus ni image surdimensionnée à réduire,
ni fenêtre de recadrage à calculer pendant la rotation 3D.

Figma : boîte 225x254, image rendue en 320x320 (source 400x400, donc
échelle 0.8), décalée de -54.54 en x et +0.46 en y.
"""
from PIL import Image
import pathlib

SRC = pathlib.Path("sources/photo-romain-source.png")
OUT = pathlib.Path("assets/photo-romain.webp")

BOITE = (225, 254)          # dimensions d'affichage dans le design
ECHELLE = 0.8               # 320 rendus / 400 source
DECALAGE = (-54.54, 0.457)  # position de l'image dans la boîte

im = Image.open(SRC).convert("RGB")

# Fenêtre visible, ramenée dans l'espace de la source
x0 = -DECALAGE[0] / ECHELLE
y0 = -DECALAGE[1] / ECHELLE
x1 = x0 + BOITE[0] / ECHELLE
y1 = y0 + BOITE[1] / ECHELLE
boite = (max(0, round(x0)), max(0, round(y0)),
         min(im.width, round(x1)), min(im.height, round(y1)))

crop = im.crop(boite)
crop.save(OUT, "WEBP", quality=86, method=6)

print(f"source {im.size[0]}x{im.size[1]} ({SRC.stat().st_size//1024} ko)")
print(f"fenêtre {boite} -> {crop.size[0]}x{crop.size[1]}")
print(f"ratio obtenu {crop.size[0]/crop.size[1]:.4f} · attendu {BOITE[0]/BOITE[1]:.4f}")
print(f"✓ {OUT} — {OUT.stat().st_size//1024} ko")
