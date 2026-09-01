# Carte de visite numérique

Carte web ajoutable à l'écran d'accueil iOS. Lumière rasante animée,
retournement 3D au toucher, vCard native, animation d'ouverture.
Aucun compte Apple Developer, aucun abonnement, aucune permission demandée.

## Modifier le contenu

1. **`config.json`** — identité, coordonnées, URL publique de la carte.
2. Régénérer les fichiers dérivés :
   ```
   python3 build.py        # -> qr.svg + contact.vcf
   python3 build-icones.py # -> icon-180.png + icon-512.png
   ```
   (`segno` et `Pillow` requis : `pip install segno pillow`)
3. **`index.html`** — les textes affichés sont en clair dans le HTML.

⚠️ `config.json` alimente le QR, la vCard et les icônes — **pas** le texte
affiché sur la carte. Les deux sont à mettre à jour.

## Régler l'apparence

Tout est dans les jetons `:root` en tête du `<style>` :

| Jeton | Rôle |
|---|---|
| `--intensite` | Force de la lumière. `.5` très discret · `1.2` par défaut · `1.6` marqué |
| `--rayon` | Angles de la carte. `0` pour des angles vifs |
| `--carte` / `--carte-haut` | Dégradé de fond de la carte |
| `--texte` / `--attenue` | Texte principal / secondaire |

## Comment fonctionne la lumière

La source lumineuse est projetée **hors** de la carte : on n'en voit que la
retombée, ce qui donne un éclairage rasant plutôt qu'une tache posée au milieu.
Elle suit une orbite à phase unique qui ne passe jamais près du centre — c'est
précisément au centre qu'un halo cesse de lire comme de la lumière.

Elle dérive seule en permanence, et suit le doigt tant qu'on touche la carte.

Pas de gyroscope : il exige une permission explicite **et** un réglage système
(Réglages → Safari → Accès au mouvement) qui peut être désactivé chez le
destinataire, sans aucun retour visible. Trop fragile pour un livrable.

## Déployer

```
npx vercel --prod
```

Puis remettre l'URL obtenue dans `urlCarte` (config.json) et relancer
`build.py` — sinon le QR du verso pointe sur l'ancienne adresse.

## Ajouter à l'écran d'accueil

Safari → Partager → « Sur l'écran d'accueil ». La carte s'ouvre en plein écran,
sans barre d'adresse.

## Puce NFC (optionnel)

Une NTAG215 (~0,50 €) collée au dos de la carte physique, encodée avec l'URL
via l'app NFC Tools. Les iPhone (XS et plus) les lisent depuis l'écran
verrouillé, sans application.

## Accessibilité

`prefers-reduced-motion` désactive l'animation d'ouverture, le balayage et les
transitions. La carte reste entièrement fonctionnelle.
