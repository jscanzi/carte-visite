# Carte de visite numérique

Carte web ajoutable à l'écran d'accueil. Effet holographique piloté par le
gyroscope, retournement 3D au toucher, vCard native.
Aucun compte Apple Developer, aucun abonnement.

## Modifier le contenu

1. **`config.json`** — identité, coordonnées, URL publique de la carte.
2. Régénérer les fichiers dérivés :
   ```
   python3 build.py        # -> qr.svg + contact.vcf
   python3 build-icones.py # -> icon-180.png + icon-512.png
   ```
   (`segno` et `Pillow` requis : `pip install segno pillow`)
3. **`index.html`** — les textes affichés sont en clair dans le HTML, à éditer
   directement. Les couleurs et le rayon des angles sont les jetons `:root`
   en haut du `<style>` (`--rayon:0` pour des angles vifs).

⚠️ `config.json` alimente le QR, la vCard et les icônes — pas le texte affiché
sur la carte. Les deux sont à mettre à jour.

## Prévisualiser

```
python3 -m http.server 4321 --directory .
```

L'effet gyroscope ne se voit que sur un vrai téléphone (sur ordinateur, la
souris pilote le repli). En HTTP local iOS refuse le capteur : passer par
l'URL de déploiement ou un tunnel HTTPS pour tester sur mobile.

## Déployer

```
npx vercel --prod
```

Puis remettre l'URL obtenue dans `urlCarte` (config.json) et relancer
`build.py` — sinon le QR du verso pointe encore sur l'exemple.

## Ajouter à l'écran d'accueil

Safari → Partager → « Sur l'écran d'accueil ». La carte s'ouvre alors en plein
écran, sans barre d'adresse.

## Puce NFC (optionnel)

Une NTAG215 (~0,50 €) collée au dos de la carte physique, encodée avec l'URL
via l'app NFC Tools. Les iPhone (XS et plus) les lisent depuis l'écran
verrouillé, sans application. La carte papier ouvre alors la carte numérique.

## Compatibilité

- Gyroscope : iOS 13+, permission demandée au premier contact. Refus ou absence
  de capteur → animation de repos + glisser du doigt, rien ne casse.
- HTTPS obligatoire pour le capteur d'orientation.
