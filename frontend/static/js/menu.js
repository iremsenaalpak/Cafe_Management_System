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
      </div>
    </div>
  `).join("");

  // click -> open modal
  grid.querySelectorAll(".menu-card").forEach(card => {
    card.addEventListener("click", () => openModal(card.dataset.id));
  });
}

function setActiveFilter(cat) {
  ACTIVE_CAT = cat;
  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.cat === cat);
  });
  renderGrid();
}

function openModal(productId) {
  const p = ALL_PRODUCTS.find(x => String(x.id) === String(productId));
  if (!p) return;

  const modal = document.getElementById("productModal");
  const closeBtn = document.getElementById("modalClose");

  document.getElementById("modalImg").src = imgUrl(p);
  document.getElementById("modalTitle").textContent = p.name || "";
  document.getElementById("modalCategory").textContent = p.category || "";
  document.getElementById("modalPrice").textContent = `${Number(p.price || 0).toFixed(0)} TL`;
  document.getElementById("modalDesc").textContent = p.description || "";

  const tagsEl = document.getElementById("modalTags");
  const labels = p.labels || [];
  tagsEl.innerHTML = labels.map(l => `<span class="modal-tag">${l}</span>`).join("");

  modal.style.display = "flex";

  const onClose = () => {
    modal.style.display = "none";
    modal.removeEventListener("click", overlayClose);
    closeBtn.removeEventListener("click", onClose);
    document.removeEventListener("keydown", escClose);
  };

  const overlayClose = (e) => {
    if (e.target === modal) onClose();
  };

  const escClose = (e) => {
    if (e.key === "Escape") onClose();
  };

  modal.addEventListener("click", overlayClose);
  closeBtn.addEventListener("click", onClose);
  document.addEventListener("keydown", escClose);
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

