# Éclat d'Or — Maison de joaillerie (site de démonstration)

Site vitrine complet et fictif réalisé par **Matrice Studio** pour présenter ses savoir-faire web.
Tous les contenus (maison, pièces, prix, avis, personnes) sont imaginaires ; aucune marque réelle n'est citée.

## Ouvrir le site

Aucun build ni backend n'est nécessaire :

- **Double-cliquez sur `index.html`** — tout fonctionne en local (polices, images et scripts sont auto-hébergés) ;
- ou servez le dossier : `python -m http.server 8000` puis http://localhost:8000.

## Pages (18)

| Page | Contenu |
|---|---|
| `index.html` | Accueil : héros, manifeste, collections, sélection, haute joaillerie, avis, rendez-vous |
| `maison.html` | Histoire (1932), frise, savoir-faire, atelier, équipe |
| `collections.html` | Boutique : 26 pièces, filtres (catégorie, collection) et tri fonctionnels |
| `piece.html?id=…` | Fiche produit : matériaux, pierres, carats, options, panier, JSON-LD produit |
| `haute-joaillerie.html` | Quatre pièces uniques, traitement éditorial |
| `sur-mesure.html` | Parcours de demande en 4 étapes avec validation et confirmation |
| `services.html` | Gravure, retouche, réparation, emballage, livraison, retours, entretien |
| `guides.html` | Tailles de bagues, entretien, 4C, métaux, certificats, éthique (sommaire actif) |
| `galerie.html` | Galerie masonry avec visionneuse (lightbox) |
| `avis.html` | Avis clients avec synthèse de notes |
| `rendez-vous.html` | Réservation boutique / visio : créneaux simulés, récapitulatif, confirmation |
| `contact.html` | Coordonnées, horaires, plan stylisé, formulaire validé |
| `panier.html` | Panier complet + commande (validation, total, récapitulatif, confirmation) |
| `favoris.html` | Liste de souhaits (persistée localement) |
| `mentions-legales.html`, `confidentialite.html`, `cgv.html` | Pages légales cohérentes avec la fiction |
| `404.html` | Page introuvable |

## Technique

- **Statique, sans dépendance** : HTML + CSS + JS vanilla (aucun framework, aucune requête externe).
- Panier et favoris en `localStorage` ; aucun paiement ni envoi de données (démonstration).
- Design system : palette ivoire/encre/or, Cormorant + Montserrat auto-hébergées (woff2), responsive 375 → 1920, `prefers-reduced-motion` respecté, focus visibles, contrastes AA.
- SEO : `lang="fr"`, métadonnées + Open Graph + Twitter Card, canoniques, JSON-LD (`JewelryStore`, `Product`), `robots.txt`, `sitemap.xml`, favicon complet + web manifest.
- Performances : images WebP optimisées, `loading="lazy"`, `fetchpriority` sur le héros, fonts `preload`.

## Régénérer les pages (optionnel)

Les pages sont déjà générées. Pour modifier les partiels partagés (en-tête, pied de page) puis régénérer :

```bash
python tools/build.py
```

Les corps de pages se trouvent dans `templates/pages/`, les partiels dans `tools/build.py`.

## Crédits

Photographies : Pexels (détail fichier par fichier dans [`SOURCES.md`](SOURCES.md)).
Contact du site : [matricestudio@protonmail.com](mailto:matricestudio@protonmail.com).

© 2026 Matrice Studio. Tous droits réservés.
