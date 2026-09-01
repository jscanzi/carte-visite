# Carte de visite numérique — Romain Legresy (Inqom)

Transposition web de la carte de visite Inqom. Ajoutable à l'écran d'accueil
iOS, retournement 3D vers le QR, vCard native, animation d'ouverture.
Aucun compte développeur, aucun abonnement, aucune permission demandée.

Source du design : fichier Figma `Carte_Visite_Inqom`, frames `Recto` (337:77)
et verso (337:127), 650 × 1004.

## Charte appliquée

| Rôle | Valeur | Nom Inqom |
|---|---|---|
| Fond recto | `#2A0F2E` | aubergine (signature) |
| Fond d'écran | `#FAF8F5` | crème |
| Intitulé de poste | `#B28FE0` | bloom-vif (accent) |
| Fond verso | `#A381CC` | lilas |
| Angles | `0` | **tout en sharp**, convention maison |

⚠️ **Trois précautions rendent le retournement fiable sur Safari iOS.** Sans
elles, les deux faces se superposent (la face arrière apparaît en miroir) :

1. `.entree` anime l'**opacité** ; elle est donc placée **hors** du contexte 3D
   (à l'extérieur de `.scene`) et porte sa propre `perspective()` dans la
   fonction `transform`. L'opacité est une propriété de groupage : sur un
   ancêtre en `preserve-3d`, elle aplatit le contexte.
2. Le rognage et le `mix-blend-mode` vivent dans `.plan` (`isolation:isolate`),
   pas sur `.face` : `overflow:hidden` et les fondus sur une face en
   `backface-visibility` cassent le rendu 3D de Safari.
3. **On ne se fie plus du tout à `backface-visibility`** : il échoue en
   pratique sur Safari iOS. **Une seule face est rendue à tout instant**
   (`opacity`), et l'échange se fait à mi-rotation, quand la carte est de
   profil — donc invisible. La courbe étant symétrique, 50 % du mouvement
   = 50 % de la durée. ⚠️ Si tu changes la durée de la transition de
   `.pivot`, mets `DUREE_ROTATION` à la même valeur, sinon l'échange se
   voit.

⚠️ **Le contenu de la carte porte ses couleurs explicitement**, il n'hérite pas
de `body` : le fond d'écran est clair, l'héritage rendrait le nom sombre sur
sombre. Ne pas retirer les `color:` de `.identite` et `.coordonnees`.

## Police de marque

La carte est composée en **Matter** (Displaay Type Foundry), licence achetée par
**Inqom** — facture DP15269, usages *Desktop + Print, Social Media, **Web***,
jusqu'à 250 personnes. L'usage Web autorise nommément l'auto-hébergement via
`@font-face`, et le partage avec les prestataires du licencié.

Fichier utilisé : `assets/MatterUprightsVF.woff2`, livré tel quel par la
fonderie. Variante *Uprights* (178 ko) plutôt que la VF complète (260 ko) :
la carte n'emploie aucune italique.

⚠️ **Ne pas convertir ni sous-ensembler la police.** La licence interdit
explicitement d'altérer, convertir ou modifier les fichiers. Displaay fournit
déjà le WOFF2, il n'y a donc rien à convertir.

⚠️ **La police n'est pas versionnée** (voir `.gitignore`). Tant que ce dépôt est
public, y committer le fichier reviendrait à le mettre à disposition de tous,
ce que la licence ne couvre pas : elle autorise l'hébergement en `@font-face`
sur le site, pas la diffusion du fichier dans un dépôt de sources ouvert.
Il faut donc déposer `MatterUprightsVF.woff2` dans `assets/` à la main, ou
passer le dépôt en privé avant de le versionner.

Sans ce fichier, la page se rabat silencieusement sur la police système.

## Modifier le contenu

1. **`config.json`** — identité, coordonnées, URL publique. Alimente le QR,
   la vCard et rien d'autre.
2. **`index.html`** — les textes affichés sont en clair dans le HTML. À mettre
   à jour **en plus** de `config.json`, les deux ne sont pas liés.
3. Régénérer les fichiers dérivés :
   ```
   python3 build.py         # -> qr.svg + contact.vcf
   python3 build-icones.py  # -> icon-180.png + icon-512.png (spark Inqom)
   python3 build-photo.py   # -> assets/photo-romain.webp (recadrage Figma)
   ```
   (`segno` et `Pillow` requis : `pip install segno pillow`)

## Régler l'apparence

Jetons `:root` en tête du `<style>` :

| Jeton | Rôle |
|---|---|
| `--intensite` | Force du reflet lumineux. `0` = aucun · `.55` par défaut · `1.2` marqué |
| `--rayon` | Angles. Reste à `0` : convention Inqom |
| `--u` | Largeur de la carte, tout le reste en dérive |

## Deux points techniques

**Le motif de fond** est le spark Inqom agrandi. Ce sont les rendus du nœud
`Union` exportés depuis Figma (`assets/forme-recto.webp`, `forme-verso.webp`),
posés en haut à gauche, pleine largeur. Calage vérifié numériquement contre le
rendu de référence : erreur 0,03/255 au recto, 0,04/255 au verso.

⚠️ **Ne pas repasser au SVG.** Le `Union` exporté en SVG porte un
`feGaussianBlur stdDeviation="25"` **qui n'existe pas dans le design** —
artefact d'export. Il donnait des arêtes molles au lieu des arêtes franches
voulues, et rastériser un filtre SVG à chaque frame de rotation coûtait cher.
`assets/forme.svg` n'est conservé que parce que `build-icones.py` y lit le
tracé du spark ; il n'est plus affiché.

⚠️ **Ces images sont opaques**, la couleur de fond y est incorporée. Changer
`--aubergine` ou `--lilas` impose de réexporter depuis Figma.

ℹ️ **Pas de `mix-blend-mode`** sur les calques d'irisation : il forçait le
compositeur à relire le fond à chaque frame. Conséquence assumée — sur le fond
clair du verso, la teinte froide vire au bleu au lieu d'éclaircir. Si ce bleu
gêne, remplacer les couleurs de `.iris.chaude` / `.iris.froide` par des valeurs
de la palette (bloom `#EBC5F2`, bloom-vif `#B28FE0`) plutôt que de remettre le
blend. Sur le recto sombre, l'écart est imperceptible.

⚠️ **La lumière est figée pendant le retournement** (`enRotation` dans le JS) :
inutile de composer un éclairage sur une carte qui tourne, autant laisser la
machine à la rotation.

⚠️ **La lumière ne repeint jamais.** Les dégradés sont **fixes** ; ce sont des
éléments de 2× la taille de la carte qu'on déplace en `translate3d`, composité
par le GPU. Animer la position d'un dégradé (première version) forçait un
repaint complet à chaque frame sur quatre éléments : c'était la cause de la
latence sur mobile. Ne pas revenir à un `background-position` animé.

⚠️ **`format-detection` est obligatoire.** Sans lui, iOS détecte le numéro de
téléphone et le transforme en lien bleu souligné, même sans balise `<a>`.

**La lumière** est un éclairage rasant : la source est projetée hors de la carte,
on n'en voit que la retombée. Elle suit une orbite à phase unique qui ne passe
jamais près du centre — c'est au centre qu'un halo cesse de lire comme de la
lumière et devient une tache. Elle dérive seule et suit le doigt au toucher.

Pas de gyroscope : il exige une permission **et** un réglage système
(Réglages → Safari → Accès au mouvement) désactivable côté destinataire, sans
retour visible. Trop fragile pour un livrable client.

## Déployer

En ligne sur GitHub Pages : https://jscanzi.github.io/carte-visite/

Pour Vercel :
```
npx vercel --prod
```
Puis reporter l'URL dans `urlCarte` (config.json) et relancer `build.py`,
sinon le QR du verso pointe sur l'ancienne adresse. `vercel.json` sert déjà la
vCard en `text/vcard`, ce que GitHub Pages ne fait pas.

## Ajouter à l'écran d'accueil

Safari → Partager → « Sur l'écran d'accueil ». Icône = spark Inqom blanc sur
aubergine ; la carte s'ouvre en plein écran, sans barre d'adresse.

## Puce NFC (optionnel)

Une NTAG215 (~0,50 €) collée au dos de la carte physique, encodée avec l'URL
via l'app NFC Tools. Les iPhone (XS et plus) les lisent depuis l'écran
verrouillé, sans application.

## Accessibilité

`prefers-reduced-motion` neutralise l'ouverture, le balayage et les transitions.

## Poids de la page

| Élément | Poids |
|---|---|
| Police Matter (Uprights VF) | 176 ko |
| Photo (WebP, recadrée en amont) | 24 ko |
| Formes de fond (2 WebP) | 20 ko |
| Logos + QR (SVG) | 32 ko |
| HTML | ~15 ko |

⚠️ **La photo est recadrée en amont** par `build-photo.py`, aux dimensions
exactes d'affichage. Elle était en PNG 400×400 de 260 ko, réduite et recadrée
par CSS à l'exécution — c'était le plus gros coût pendant la rotation.
La source reste dans `sources/` pour pouvoir régénérer.

ℹ️ Aucune requête externe : ni Google Fonts, ni CDN.
