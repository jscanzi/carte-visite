#!/usr/bin/env python3
"""Icônes d'écran d'accueil : le spark Inqom blanc sur aubergine.

Le tracé est repris tel quel de assets/forme.svg. Il n'emploie que des
commandes absolues M/H/L/C/Z, donc un petit aplatissement des cubiques
suffit — pas besoin d'un moteur SVG.
"""
import re, pathlib
from PIL import Image, ImageDraw

AUBERGINE = (0x2A, 0x0F, 0x2E)
BLANC     = (0xFF, 0xFF, 0xFF)
MARGE     = .20          # part du côté laissée vide autour du spark

def lire_trace(svg_path):
    d = re.search(r'\sd="([^"]+)"', pathlib.Path(svg_path).read_text()).group(1)
    jetons = re.findall(r'([MHLCZ])|(-?\d*\.?\d+)', d)
    sortie, i = [], 0
    plat = [(c or n) for c, n in jetons]
    pts, cur, cmd = [], (0.0, 0.0), None

    def cubique(p0, p1, p2, p3, n=24):
        for k in range(1, n + 1):
            t = k / n; u = 1 - t
            yield (u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
                   u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1])

    while i < len(plat):
        j = plat[i]
        if j in "MHLCZ":
            cmd = j; i += 1; continue
        if cmd == "M":
            cur = (float(plat[i]), float(plat[i+1])); pts.append(cur); i += 2
        elif cmd == "L":
            cur = (float(plat[i]), float(plat[i+1])); pts.append(cur); i += 2
        elif cmd == "H":
            cur = (float(plat[i]), cur[1]); pts.append(cur); i += 1
        elif cmd == "C":
            p1 = (float(plat[i]),   float(plat[i+1]))
            p2 = (float(plat[i+2]), float(plat[i+3]))
            p3 = (float(plat[i+4]), float(plat[i+5]))
            pts.extend(cubique(cur, p1, p2, p3)); cur = p3; i += 6
        else:
            i += 1
    return pts

def icone(taille, pts, boite):
    (x0, y0, x1, y1) = boite
    img = Image.new("RGB", (taille, taille), AUBERGINE)
    d = ImageDraw.Draw(img)
    dispo = taille * (1 - MARGE * 2)
    k = min(dispo / (x1 - x0), dispo / (y1 - y0))
    dx = (taille - (x1 - x0) * k) / 2 - x0 * k
    dy = (taille - (y1 - y0) * k) / 2 - y0 * k
    d.polygon([(p[0]*k + dx, p[1]*k + dy) for p in pts], fill=BLANC)
    img.save(f"icon-{taille}.png")
    print(f"✓ icon-{taille}.png — spark Inqom blanc sur aubergine")

pts = lire_trace("assets/forme.svg")
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
boite = (min(xs), min(ys), max(xs), max(ys))
print(f"tracé : {len(pts)} points, boîte {tuple(round(v) for v in boite)}")
for t in (180, 512):
    icone(t, pts, boite)
