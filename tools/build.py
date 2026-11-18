# -*- coding: utf-8 -*-
"""Générateur de pages statiques pour le site Éclat d'Or.
Usage : python tools/build.py   (depuis la racine du site)
"""
import os, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(ROOT, "templates", "pages")

BASE_URL = "https://www.eclatdor-paris.fr"
SITE_NAME = "Éclat d'Or"

def head(p):
    og_type = "website"
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['title']}</title>
  <meta name="description" content="{p['description']}">
  <link rel="canonical" href="{BASE_URL}/{p['slug'] if p['slug'] != 'index' else ''}">
  <meta name="theme-color" content="#14100C">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:title" content="{p['title']}">
  <meta property="og:description" content="{p['description']}">
  <meta property="og:url" content="{BASE_URL}/{p['slug'] if p['slug'] != 'index' else ''}">
  <meta property="og:image" content="{BASE_URL}/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{p['title']}">
  <meta name="twitter:description" content="{p['description']}">
  <meta name="twitter:image" content="{BASE_URL}/og-image.jpg">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" href="favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="preload" href="assets/fonts/cormorant-500.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/style.css">
  {p.get('schema', '')}
</head>
<body class="{p.get('body_class', '')}">
<a class="skip-link" href="#contenu">Aller au contenu principal</a>
"""

LOGO_SVG = """<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><defs><linearGradient id="or" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D8B77C"/><stop offset=".5" stop-color="#B08D57"/><stop offset="1" stop-color="#8A6A3B"/></linearGradient></defs><g fill="none" stroke="url(#or)" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"><path d="M10 22 L21 9 L43 9 L54 22 L32 55 Z"/><path d="M10 22 H54"/><path d="M21 9 L27 22 M43 9 L37 22"/><path d="M27 22 L32 55 M37 22 L32 55"/><path d="M52 6 V14 M48 10 H56" stroke-width="2"/></g></svg>"""

NAV = [
    ("index", "Accueil", "index.html"),
    ("maison", "La Maison", "maison.html"),
    ("collections", "Boutique", "collections.html"),
    ("haute", "Haute Joaillerie", "haute-joaillerie.html"),
    ("surmesure", "Sur Mesure", "sur-mesure.html"),
    ("guides", "Guides", "guides.html"),
    ("galerie", "Galerie", "galerie.html"),
    ("contact", "Contact", "contact.html"),
]

def header(p):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if p["slug"] == key else ""}>{label}</a>'
        for key, label, href in NAV
    )
    current = p["slug"]
    mobile_links = ""
    for i, (key, label, href) in enumerate([
        ("index", "Accueil", "index.html"),
        ("maison", "La Maison", "maison.html"),
        ("collections", "Boutique", "collections.html"),
        ("haute", "Haute Joaillerie", "haute-joaillerie.html"),
        ("surmesure", "Sur Mesure", "sur-mesure.html"),
        ("services", "Services", "services.html"),
        ("guides", "Guides", "guides.html"),
        ("galerie", "Galerie", "galerie.html"),
        ("avis", "Avis clients", "avis.html"),
        ("rendez-vous", "Rendez-vous", "rendez-vous.html"),
        ("contact", "Contact", "contact.html"),
    ], 1):
        mobile_links += f'<a href="{href}">{label}<span class="num">0{i}</span></a>\n'
    return f"""
<header class="site-header{' site-header--solid' if current != 'index' else ''}">
  <div class="container">
    <a class="brand" href="index.html" aria-label="Éclat d'Or — Accueil">
      {LOGO_SVG}
      <span>
        <span class="brand-name">Éclat d&rsquo;Or</span>
        <span class="brand-sub">Joaillerie · Paris</span>
      </span>
    </a>
    <nav class="nav-desktop" aria-label="Navigation principale">
      {links}
      <a class="btn btn--outline" href="rendez-vous.html">Rendez-vous</a>
    </nav>
    <div class="header-actions">
      <a class="icon-btn" href="favoris.html" aria-label="Mes favoris">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21c-4.9-3.4-9-6.7-9-11a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 4.3-4.1 7.6-9 11z"/></svg>
        <span class="badge-count" data-wish-count data-empty="true">0</span>
      </a>
      <button class="icon-btn" type="button" data-open-cart aria-label="Ouvrir le panier">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 8h12l-1 13H7L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>
        <span class="badge-count" data-cart-count data-empty="true">0</span>
      </button>
      <button class="icon-btn nav-toggle" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu-mobile">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h10"/></svg>
      </button>
    </div>
  </div>
</header>

<div class="nav-mobile" id="menu-mobile" aria-label="Menu mobile">
  <div class="nav-mobile-top">
    <a class="brand" href="index.html" aria-label="Éclat d'Or — Accueil">{LOGO_SVG}<span><span class="brand-name">Éclat d&rsquo;Or</span></span></a>
    <button class="icon-btn" type="button" data-close-nav aria-label="Fermer le menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
  </div>
  <nav aria-label="Navigation mobile">
    {mobile_links}
  </nav>
  <div class="nav-mobile-footer">
    <a class="btn btn--gold" href="rendez-vous.html">Prendre rendez-vous</a>
    <a class="btn btn--outline" href="collections.html">Explorer la boutique</a>
  </div>
</div>

<main id="contenu">
"""

def footer(p):
    return f"""
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="index.html" style="color:var(--ivory)">{LOGO_SVG}<span><span class="brand-name">Éclat d&rsquo;Or</span><span class="brand-sub">Joaillerie · Paris</span></span></a>
        <p>Depuis 1932, notre atelier façonne des bijoux destinés à traverser le temps — et à être transmis.</p>
        <h3>Lettre de la maison</h3>
        <p>Nouvelles collections, carnets d&rsquo;atelier et invitations privées, une fois par saison.</p>
        <form class="news-form" novalidate>
          <label class="skip-link" for="news-email">Votre adresse e-mail</label>
          <input type="email" id="news-email" name="email" placeholder="votre@email.fr" autocomplete="email" required>
          <button type="submit">S&rsquo;inscrire</button>
        </form>
      </div>
      <div>
        <h3>La Maison</h3>
        <ul class="footer-links">
          <li><a href="maison.html">Notre histoire</a></li>
          <li><a href="maison.html#savoir-faire">Savoir-faire &amp; atelier</a></li>
          <li><a href="maison.html#equipe">Artisans &amp; équipe</a></li>
          <li><a href="haute-joaillerie.html">Haute joaillerie</a></li>
          <li><a href="galerie.html">Galerie</a></li>
          <li><a href="avis.html">Avis clients</a></li>
        </ul>
      </div>
      <div>
        <h3>Boutique</h3>
        <ul class="footer-links">
          <li><a href="collections.html">Toutes les pièces</a></li>
          <li><a href="collections.html?cat=bagues">Bagues</a></li>
          <li><a href="collections.html?cat=colliers">Colliers</a></li>
          <li><a href="collections.html?cat=bracelets">Bracelets</a></li>
          <li><a href="collections.html?cat=montres">Montres</a></li>
          <li><a href="favoris.html">Mes favoris</a></li>
          <li><a href="panier.html">Mon panier</a></li>
        </ul>
      </div>
      <div>
        <h3>Services &amp; Contact</h3>
        <ul class="footer-links">
          <li><a href="sur-mesure.html">Création sur mesure</a></li>
          <li><a href="rendez-vous.html">Prendre rendez-vous</a></li>
          <li><a href="services.html">Gravure, retouche, réparation</a></li>
          <li><a href="guides.html">Guides du joaillier</a></li>
          <li><a href="services.html#livraison">Livraison &amp; retours</a></li>
          <li><a href="contact.html">Nous écrire</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Matrice Studio. Tous droits réservés.</span>
      <nav class="legal-links" aria-label="Liens légaux">
        <a href="mentions-legales.html">Mentions légales</a>
        <a href="confidentialite.html">Confidentialité</a>
        <a href="cgv.html">Conditions de vente</a>
      </nav>
      <div class="footer-cta-row">
        <a class="projects-btn" href="https://www.example.com" target="_blank" rel="noopener noreferrer">Découvrir nos autres projets
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9"/><path d="M20 14v6H4V4h6"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>

<div class="toast-zone" hidden></div>
<script src="assets/js/products.js" defer></script>
<script src="assets/js/main.js" defer></script>
{p.get('scripts', '')}
</body>
</html>
"""

PAGES = [
    dict(slug="index",             file="index.html",             title="Éclat d'Or — Maison de joaillerie à Paris depuis 1932", description="Maison de joaillerie parisienne indépendante : collections d'or et de diamants, haute joaillerie en pièces uniques, création sur mesure et atelier d'exception depuis 1932."),
    dict(slug="maison",            file="maison.html",            title="La Maison — Histoire & savoir-faire | Éclat d'Or", description="Découvrez l'histoire d'Éclat d'Or depuis 1932, notre atelier parisien, nos artisans joailliers, sertisseurs et polisseurs, et les gestes qui font nos créations."),
    dict(slug="collections",       file="collections.html",       title="Boutique — Collections de joaillerie | Éclat d'Or", description="Explorez nos bagues, colliers, bracelets, boucles d'oreilles et montres en or 18 carats sertis de pierres certifiées. Filtres par catégorie, matière et prix."),
    dict(slug="piece",             file="piece.html",             title="Fiche produit | Éclat d'Or", description="Fiche détaillée d'une création Éclat d'Or : matériaux, pierres, carats, dimensions et prix. Sertie à la main dans notre atelier parisien."),
    dict(slug="haute-joaillerie",  file="haute-joaillerie.html",  title="Haute Joaillerie — Pièces uniques | Éclat d'Or", description="Entrez dans l'atelier d'exception d'Éclat d'Or : quatre pièces uniques de haute joaillerie, centaines d'heures d'atelier, pierres d'exception certifiées."),
    dict(slug="sur-mesure",        file="sur-mesure.html",        title="Création sur mesure | Éclat d'Or", description="Dessinez votre propre joaillerie avec nos maîtres artisans : parcours en cinq étapes, du premier croquis à l'écrin final. Bague de fiançailles, alliance, pièce d'exception."),
    dict(slug="services",          file="services.html",          title="Services — Gravure, entretien, réparation | Éclat d'Or", description="Gravure personnalisée, retouche de taille, réparation d'atelier, emballage cadeau, livraison assurée et retours sous 30 jours : les services d'Éclat d'Or."),
    dict(slug="guides",            file="guides.html",            title="Guides du joaillier — Tailles, entretien, pierres | Éclat d'Or", description="Guides pratiques d'Éclat d'Or : trouver sa taille de bague, entretenir ses bijoux, comprendre la qualité des pierres et des métaux, certificats et éthique d'approvisionnement."),
    dict(slug="galerie",           file="galerie.html",           title="Galerie — L'or en images | Éclat d'Or", description="Portraits, mains, éclats et coulisses : la galerie photographique de la maison Éclat d'Or."),
    dict(slug="avis",              file="avis.html",              title="Avis clients | Éclat d'Or", description="Ce que nos clients disent de la maison : fiançailles, créations sur mesure, réparations et accueil en boutique, à Paris et ailleurs."),
    dict(slug="rendez-vous",       file="rendez-vous.html",       title="Prendre rendez-vous — Boutique ou visioconférence | Éclat d'Or", description="Réservez un créneau privé avec un conseiller joaillier, en boutique au 9 square Vendôme à Paris ou en visioconférence. Confirmation immédiate."),
    dict(slug="contact",           file="contact.html",           title="Contact | Éclat d'Or", description="Écrivez à la maison Éclat d'Or : 9 square Vendôme, 75009 Paris. Questions, devis sur mesure, presse et partenariats."),
    dict(slug="panier",            file="panier.html",            title="Panier & commande | Éclat d'Or", description="Votre panier Éclat d'Or : récapitulatif, livraison offerte dès 500 €, emballage cadeau et commande en quelques instants."),
    dict(slug="favoris",           file="favoris.html",           title="Mes favoris | Éclat d'Or", description="Les créations Éclat d'Or que vous avez mises de côté : retrouvez-les ici, partagez-les ou passez commande."),
    dict(slug="mentions-legales",  file="mentions-legales.html",  title="Mentions légales | Éclat d'Or", description="Mentions légales du site Éclat d'Or, maison de joaillerie fictive — démonstration réalisée par Matrice Studio."),
    dict(slug="confidentialite",   file="confidentialite.html",   title="Politique de confidentialité | Éclat d'Or", description="Comment Éclat d'Or traite vos données personnelles : finalités, durées de conservation, droits et contacts."),
    dict(slug="cgv",               file="cgv.html",               title="Conditions générales de vente | Éclat d'Or", description="Conditions générales de vente d'Éclat d'Or : commande, prix, livraison, retours, garanties et médiation de la consommation."),
    dict(slug="404",               file="404.html",               title="Page introuvable | Éclat d'Or", description="Cette page n'existe pas ou plus. Retrouvez nos collections, notre histoire et nos services sur le site d'Éclat d'Or.", body_class="page-404"),
]

SCHEMA_ORG = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "JewelryStore",
  "name": "Éclat d'Or",
  "description": "Maison de joaillerie parisienne indépendante fondée en 1932 : collections, haute joaillerie en pièces uniques et création sur mesure.",
  "url": "https://www.eclatdor-paris.fr",
  "logo": "https://www.eclatdor-paris.fr/favicon.svg",
  "image": "https://www.eclatdor-paris.fr/og-image.jpg",
  "foundingDate": "1932",
  "priceRange": "€€€€",
  "currenciesAccepted": "EUR",
  "paymentAccepted": "Carte bancaire, Virement",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "9, square Vendôme",
    "postalCode": "75009",
    "addressLocality": "Paris",
    "addressCountry": "FR"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 48.8698, "longitude": 2.3312 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "10:30", "closes": "19:00" }
  ],
  "sameAs": []
}
</script>"""

def build():
    for p in PAGES:
        body_path = os.path.join(PAGES_DIR, p["file"])
        if not os.path.exists(body_path):
            print(f"!! corps manquant : {body_path}")
            continue
        with io.open(body_path, encoding="utf-8") as f:
            body = f.read()
        if p["slug"] == "index":
            p["schema"] = SCHEMA_ORG
        html = head(p) + header(p) + body + footer(p)
        out = os.path.join(ROOT, p["file"])
        with io.open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print(f"OK {p['file']}")

if __name__ == "__main__":
    build()
