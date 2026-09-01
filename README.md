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
3. Au repos, **une seule face est rendue** (`opacity`), les deux uniquement
   pendant la rotation via la classe `.enrotation` posée par le JS. Ce filet
   ne dépend d'aucun calage temporel. Si tu changes la durée de la transition
   de `.pivot`, mets `DUREE_ROTATION` à la même valeur.

⚠️ **Le contenu de la carte porte ses couleurs explicitement**, il n'hérite pas
de `body` : le fond d'écran est clair, l'héritage rendrait le nom sombre sur
sombre. Ne pas retirer les `color:` de `.identite` et `.coordonnees`.

⚠️ **Police de marque.** Le design est composé en **Matter VF**, qui n'est pas
embarquée ici faute de licence web. La pile de repli est Inter — le proxy déjà
retenu dans Figma pour le deck et la newsletter. Dès que le `.woff2` Matter est
disponible : le déposer dans `assets/` et décommenter le bloc `@font-face` en
tête du `<style>`. Tout bascule ensuite automatiquement.

## Modifier le contenu

1. **`config.json`** — identité, coordonnées, URL publique. Alimente le QR,
   la vCard et rien d'autre.
2. **`index.html`** — les textes affichés sont en clair dans le HTML. À mettre
   à jour **en plus** de `config.json`, les deux ne sont pas liés.
3. Régénérer les fichiers dérivés :
   ```
   python3 build.py         # -> qr.svg + contact.vcf
   python3 build-icones.py  # -> icon-180.png + icon-512.png (spark Inqom)
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

**Le motif de fond** est le spark Inqom agrandi (`assets/forme.svg`), avec son
flou gaussien et son dégradé aubergine → transparent d'origine. Les unités
`hypot()` du code exporté par Figma ne se transposent pas en CSS : le placement
a été obtenu par **ajustement numérique** contre le rendu Figma (erreur moyenne
2,6/255 au recto, 5,3/255 au verso). Ne pas « corriger » ces valeurs à vue.

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
