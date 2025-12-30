let ALL_PRODUCTS = [];
let ACTIVE_CAT = "All";

function catMatches(p, cat) {
  if (cat === "All") return true;
  return (p.category || "") === cat;
}

function imgUrl(p) {
  // DB'den gelen image: "/static/images/uploads/xxx.jpg" gibi
  // boşsa fallback
  if (p.image && p.image.startsWith("/static/")) return p.image;
  if (p.image) return `/static/images/${p.image}`;
  return "/static/images/placeholder.jpg";
}

function renderGrid() {
  const grid = document.getElementById("menuGrid");
  if (!grid) return;

  const items = ALL_PRODUCTS.filter(p => catMatches(p, ACTIVE_CAT));

  if (!items.length) {
    grid.innerHTML = `<p style="color:#666;font-weight:600;">No products yet. Please add products from Admin Panel.</p>`;
    return;
  }

  grid.innerHTML = items.map(p => `
    <div class="menu-card" data-id="${p.id}">
      <img src="${imgUrl(p)}" alt="${p.name}">
      <div class="card-info">
        <h3>${p.name}</h3>
        <div class="card-category">${p.category}</div>
        <div class="card-price">${Number(p.price || 0).toFixed(0)} TL</div>
      </div>
    </div>
  `).join("");

  // click -> open modal
  grid.querySelectorAll(".menu-card").forEach(card => {
    card.addEventListener("click", () => {
      const productId = card.dataset.id;
      const p = ALL_PRODUCTS.find(x => String(x.id) === String(productId));
      if (p && window.openProductModal) {
        window.openProductModal(p);
      }
    });
  });
}

function setActiveFilter(cat) {
  ACTIVE_CAT = cat;
  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.cat === cat);
  });
  renderGrid();
}

async function loadProducts() {
  const res = await fetch("/api/products");
  ALL_PRODUCTS = await res.json();
  renderGrid();
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("menuFilters")?.addEventListener("click", (e) => {
    const btn = e.target.closest(".filter-btn");
    if (!btn) return;
    setActiveFilter(btn.dataset.cat);
  });

  loadProducts().catch(() => {
    const grid = document.getElementById("menuGrid");
    if (grid) grid.innerHTML = `<p style="color:#666;font-weight:600;">Could not load products.</p>`;
  });
});

