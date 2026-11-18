/* ============================================================
   Éclat d'Or — Socle d'interface
   Panier, favoris, navigation, toasts, révélations au scroll.
   Site de démonstration : aucune donnée n'est transmise.
   ============================================================ */
(function () {
  "use strict";
  window.ECLAT = window.ECLAT || {};

  /* ---------- Stockage sûr ---------- */
  const store = {
    get(key, fallback) {
      try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; }
      catch (e) { return fallback; }
    },
    set(key, value) {
      try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* mode privé */ }
    }
  };
  ECLAT.store = store;

  const fmtPrix = n => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n);
  ECLAT.fmtPrix = fmtPrix;

  /* ---------- Panier ---------- */
  const cart = {
    items() { return store.get("eclat-cart", []); },
    save(items) {
      store.set("eclat-cart", items);
      document.dispatchEvent(new CustomEvent("eclat:cart"));
    },
    add(id, qty = 1, opts = {}) {
      const items = this.items();
      const found = items.find(i => i.id === id && JSON.stringify(i.opts) === JSON.stringify(opts));
      if (found) found.qty = Math.min(10, found.qty + qty);
      else items.push({ id, qty, opts });
      this.save(items);
    },
    remove(index) { const items = this.items(); items.splice(index, 1); this.save(items); },
    setQty(index, qty) { const items = this.items(); if (items[index]) { items[index].qty = Math.min(10, Math.max(1, qty)); this.save(items); } },
    clear() { this.save([]); },
    count() { return this.items().reduce((s, i) => s + i.qty, 0); },
    total() {
      return this.items().reduce((s, i) => {
        const p = (ECLAT.PRODUITS || []).find(p => p.id === i.id);
        return s + (p ? p.prix * i.qty : 0);
      }, 0);
    }
  };
  ECLAT.cart = cart;

  /* ---------- Favoris ---------- */
  const wishes = {
    list() { return store.get("eclat-wishes", []); },
    has(id) { return this.list().includes(id); },
    toggle(id) {
      let l = this.list();
      l = l.includes(id) ? l.filter(x => x !== id) : [...l, id];
      store.set("eclat-wishes", l);
      document.dispatchEvent(new CustomEvent("eclat:wishes"));
      return l.includes(id);
    }
  };
  ECLAT.wishes = wishes;

  /* ---------- Icônes ---------- */
  const ICONS = {
    heart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path class="fill" d="M12 21c-4.9-3.4-9-6.7-9-11a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 4.3-4.1 7.6-9 11z" fill="currentColor" stroke="none"/><path d="M12 21c-4.9-3.4-9-6.7-9-11a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 4.3-4.1 7.6-9 11z"/></svg>',
    bag: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 8h12l-1 13H7L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4.2-4.2"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h10"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m4 12.5 5.5 5.5L20 6.5"/></svg>',
    gem: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><path d="M10 22 L21 9 L43 9 L54 22 L32 55 Z"/><path d="M10 22 H54 M21 9 L27 22 M43 9 L37 22 M27 22 L32 55 M37 22 L32 55"/></svg>',
    star: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9z"/></svg>',
    starEmpty: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9z"/></svg>',
    external: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9"/><path d="M20 14v6H4V4h6"/></svg>',
    shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 2l8 3v6c0 5-3.4 9.4-8 11-4.6-1.6-8-6-8-11V5l8-3z"/><path d="m8.5 12 2.5 2.5L15.5 10"/></svg>'
  };
  ECLAT.icon = name => ICONS[name] || "";

  const etoiles = (note, cls = "stars") => {
    let s = `<span class="${cls}" role="img" aria-label="${note} étoiles sur 5">`;
    for (let i = 1; i <= 5; i++) s += i <= note ? ICONS.star : ICONS.starEmpty;
    return s + "</span>";
  };
  ECLAT.etoiles = etoiles;

  /* ---------- Toasts ---------- */
  let toastZone = null;
  function toast(html, linkLabel, linkHref) {
    if (!toastZone) {
      toastZone = document.createElement("div");
      toastZone.className = "toast-zone";
      toastZone.setAttribute("role", "status");
      toastZone.setAttribute("aria-live", "polite");
      document.body.appendChild(toastZone);
    }
    const el = document.createElement("div");
    el.className = "toast";
    el.innerHTML = `<span>${ICONS.check}</span><span>${html}</span>`;
    if (linkLabel && linkHref) {
      const a = document.createElement("a");
      a.href = linkHref; a.textContent = linkLabel;
      el.appendChild(a);
    }
    toastZone.appendChild(el);
    setTimeout(() => { el.classList.add("is-leaving"); setTimeout(() => el.remove(), 320); }, 3800);
  }
  ECLAT.toast = toast;

  /* ---------- Formatage carte produit ---------- */
  const CATS = {
    "bagues": "Bague",
    "colliers": "Collier",
    "bracelets": "Bracelet",
    "boucles-doreilles": "Boucles d'oreilles",
    "montres": "Montre",
    "haute-joaillerie": "Haute joaillerie"
  };
  ECLAT.cats = CATS;

  function productCard(p, opts = {}) {
    const wished = wishes.has(p.id);
    const fig = document.createElement("article");
    fig.className = "product-card reveal";
    fig.innerHTML = `
      <div class="product-card__media">
        <div class="product-card__flags">
          ${p.nouveaute ? '<span class="flag flag--gold">Nouveauté</span>' : ""}
          ${p.coupDeCoeur ? '<span class="flag">Coup de cœur</span>' : ""}
          ${p.categorie === "haute-joaillerie" ? '<span class="flag">Pièce unique</span>' : ""}
        </div>
        <button class="wish-btn" type="button" aria-pressed="${wished}" aria-label="Ajouter ${p.nom} aux favoris" data-wish="${p.id}">${ICONS.heart}</button>
        <a href="piece.html?id=${encodeURIComponent(p.id)}" tabindex="-1" aria-hidden="true">
          <img src="${p.image}" alt="${p.nom} — ${p.pierre !== "—" ? p.pierre : p.matiere}" loading="lazy" width="900" height="1200">
        </a>
      </div>
      <div class="product-card__body">
        <span class="product-card__cat">${CATS[p.categorie] || p.categorie} · ${p.collection}</span>
        <h3 class="product-card__name"><a href="piece.html?id=${encodeURIComponent(p.id)}">${p.nom}</a></h3>
        <span class="product-card__meta">${p.pierre !== "—" ? p.pierre : p.matiere}</span>
        <span class="product-card__price">${fmtPrix(p.prix)} ${opts.tax ? '<small>TTC, écrin offert</small>' : ""}</span>
      </div>`;
    return fig;
  }
  ECLAT.productCard = productCard;

  /* ---------- Drawer panier ---------- */
  let drawerEl = null;
  function buildDrawer() {
    drawerEl = document.createElement("div");
    drawerEl.className = "drawer";
    drawerEl.id = "cart-drawer";
    drawerEl.setAttribute("aria-hidden", "true");
    drawerEl.innerHTML = `
      <button class="drawer__veil" type="button" aria-label="Fermer le panier" data-close-drawer></button>
      <aside class="drawer__panel" role="dialog" aria-modal="true" aria-label="Panier">
        <header class="drawer__head">
          <h2>Votre sélection</h2>
          <button class="icon-btn" type="button" aria-label="Fermer le panier" data-close-drawer>${ICONS.close}</button>
        </header>
        <div class="drawer__body" data-cart-items></div>
        <footer class="drawer__foot">
          <div class="cart-totals">
            <div><span>Sous-total</span><b data-cart-subtotal>0 €</b></div>
            <div class="small" style="color:var(--muted)"><span>Livraison assurée</span><span>Offerte dès 500 €</span></div>
          </div>
          <a class="btn" href="panier.html">Voir le panier &amp; commander</a>
        </footer>
      </aside>`;
    document.body.appendChild(drawerEl);
    drawerEl.addEventListener("click", e => { if (e.target.closest("[data-close-drawer]")) closeDrawer(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && drawerEl.classList.contains("is-open")) closeDrawer(); });
    document.addEventListener("eclat:cart", renderDrawer);
  }

  function openDrawer() {
    if (!drawerEl) buildDrawer();
    renderDrawer();
    drawerEl.classList.add("is-open");
    drawerEl.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    const first = drawerEl.querySelector("button, a");
    if (first) first.focus();
  }
  function closeDrawer() {
    if (!drawerEl) return;
    drawerEl.classList.remove("is-open");
    drawerEl.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }
  ECLAT.openCart = openDrawer;

  function renderDrawer() {
    if (!drawerEl) return;
    const body = drawerEl.querySelector("[data-cart-items]");
    const items = cart.items();
    if (!items.length) {
      body.innerHTML = `<div class="cart-empty">${ICONS.gem}<p>Votre sélection est vide.</p><p class="small">Laissez-vous guider par nos collections.</p><a class="btn btn--outline btn--sm" href="collections.html">Explorer la boutique</a></div>`;
    } else {
      body.innerHTML = "";
      items.forEach((it, idx) => {
        const p = (ECLAT.PRODUITS || []).find(p => p.id === it.id);
        if (!p) return;
        const line = document.createElement("div");
        line.className = "cart-line";
        const optTxt = it.opts && (it.opts.taille || it.opts.gravure) ?
          Object.entries(it.opts).filter(([, v]) => v).map(([k, v]) => `${k === "taille" ? "Taille" : "Gravure"} : ${v}`).join(" · ") : "";
        line.innerHTML = `
          <img src="${p.image}" alt="" width="84" height="105" loading="lazy">
          <div>
            <span class="cat">${CATS[p.categorie] || ""}</span>
            <h3>${p.nom}</h3>
            ${optTxt ? `<span class="opts">${optTxt}</span>` : ""}
            <span class="price">${fmtPrix(p.prix)} × ${it.qty}</span>
          </div>
          <div class="line-actions">
            <button class="line-remove" type="button" data-remove="${idx}">Retirer</button>
          </div>`;
        body.appendChild(line);
      });
      body.querySelectorAll("[data-remove]").forEach(b =>
        b.addEventListener("click", () => { cart.remove(+b.dataset.remove); }));
    }
    drawerEl.querySelector("[data-cart-subtotal]").textContent = fmtPrix(cart.total());
  }
  ECLAT.renderDrawer = renderDrawer;

  /* ---------- Compteurs badges ---------- */
  function refreshBadges() {
    document.querySelectorAll("[data-cart-count]").forEach(b => {
      const n = cart.count();
      b.textContent = n;
      b.dataset.empty = n === 0;
      b.classList.add("pop");
      setTimeout(() => b.classList.remove("pop"), 260);
    });
    document.querySelectorAll("[data-wish-count]").forEach(b => {
      const n = wishes.list().length;
      b.textContent = n;
      b.dataset.empty = n === 0;
    });
  }
  document.addEventListener("eclat:cart", refreshBadges);
  document.addEventListener("eclat:wishes", refreshBadges);

  /* ---------- Initialisation commune ---------- */
  function init() {
    // header scroll
    const header = document.querySelector(".site-header");
    if (header && !header.classList.contains("site-header--solid")) {
      const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 24);
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }

    // menu mobile
    const toggle = document.querySelector(".nav-toggle");
    const mobile = document.querySelector(".nav-mobile");
    if (toggle && mobile) {
      const closeBtn = mobile.querySelector("[data-close-nav]");
      const setOpen = open => {
        mobile.classList.toggle("is-open", open);
        document.body.style.overflow = open ? "hidden" : "";
        toggle.setAttribute("aria-expanded", String(open));
      };
      toggle.addEventListener("click", () => setOpen(true));
      if (closeBtn) closeBtn.addEventListener("click", () => setOpen(false));
      mobile.addEventListener("click", e => { if (e.target.closest("a")) setOpen(false); });
      document.addEventListener("keydown", e => { if (e.key === "Escape") setOpen(false); });
    }

    // révélation au scroll
    const revealEls = document.querySelectorAll(".reveal");
    if (revealEls.length && "IntersectionObserver" in window) {
      const io = new IntersectionObserver(entries => {
        entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); } });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px" });
      revealEls.forEach(el => io.observe(el));
    } else {
      revealEls.forEach(el => el.classList.add("is-visible"));
    }

    // boutons favoris (délégation)
    document.addEventListener("click", e => {
      const btn = e.target.closest("[data-wish]");
      if (!btn) return;
      e.preventDefault();
      const id = btn.dataset.wish;
      const on = wishes.toggle(id);
      btn.setAttribute("aria-pressed", String(on));
      const p = (ECLAT.PRODUITS || []).find(p => p.id === id);
      toast(on ? `<b>${p ? p.nom : "La pièce"}</b> ajoutée à vos favoris` : "Retiré de vos favoris", "Voir mes favoris", "favoris.html");
    });

    // ajout panier (délégation)
    document.addEventListener("click", e => {
      const btn = e.target.closest("[data-add-cart]");
      if (!btn) return;
      e.preventDefault();
      const id = btn.dataset.addCart;
      const qty = btn.dataset.qty ? +btn.dataset.qty : 1;
      const p = (ECLAT.PRODUITS || []).find(p => p.id === id);
      cart.add(id, qty);
      toast(`<b>${p ? p.nom : "La pièce"}</b> ajoutée à votre panier`, "Voir le panier", "panier.html");
    });

    // boutons panier header
    document.querySelectorAll("[data-open-cart]").forEach(b =>
      b.addEventListener("click", e => { e.preventDefault(); openDrawer(); }));

    // newsletter (démonstration)
    document.querySelectorAll(".news-form").forEach(f => {
      f.addEventListener("submit", e => {
        e.preventDefault();
        const input = f.querySelector("input[type='email']");
        if (!input || !input.value || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(input.value)) {
          toast("Veuillez saisir une adresse e-mail valide.");
          return;
        }
        toast("Merci ! Vous recevrez nos prochaines nouvelles.");
        f.reset();
      });
    });

    refreshBadges();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
