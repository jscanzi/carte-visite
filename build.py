#!/usr/bin/env python3
"""Régénère qr.svg + contact.vcf depuis config.json. Un seul point d'entrée."""
import json, pathlib, segno

cfg = json.loads(pathlib.Path("config.json").read_text(encoding="utf-8"))

# ---------- QR (un seul <path>, fill=currentColor pour hériter du thème) ----------
qr = segno.make(cfg["urlCarte"], error="h")
m = qr.matrix; n = len(m); d = []
for y, row in enumerate(m):
    x = 0
    while x < n:
        if row[x]:
            r = x
            while r < n and row[r]:
                r += 1
            d.append(f"M{x} {y}h{r-x}v1h-{r-x}z"); x = r
        else:
            x += 1
pathlib.Path("qr.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" '
    f'shape-rendering="crispEdges" role="img" aria-label="QR code">'
    f'<path fill="currentColor" d="{"".join(d)}"/></svg>', encoding="utf-8")

# ---------- vCard 3.0 (le format qu'iOS avale sans broncher) ----------
v = [
    "BEGIN:VCARD", "VERSION:3.0",
    f'N:{cfg["nom"]};{cfg["prenom"]};;;',
    f'FN:{cfg["prenom"]} {cfg["nom"]}',
    f'ORG:{cfg["societe"]}',
    f'TITLE:{cfg["poste"]}',
    f'TEL;TYPE=CELL,VOICE:{cfg["telephone"]}',
    f'EMAIL;TYPE=INTERNET,WORK:{cfg["email"]}',
    f'URL:{cfg["site"]}',
    f'item1.URL:{cfg["linkedin"]}', "item1.X-ABLabel:LinkedIn",
    f'ADR;TYPE=WORK:;;{cfg["adresse"]};;;;',
    "END:VCARD",
]
pathlib.Path("contact.vcf").write_text("\r\n".join(v) + "\r\n", encoding="utf-8")

print(f'✓ qr.svg ({n}×{n} modules) → {cfg["urlCarte"]}')
print(f'✓ contact.vcf → {cfg["prenom"]} {cfg["nom"]}')
