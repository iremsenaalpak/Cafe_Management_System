let ALL_PRODUCTS = [];
let ACTIVE_CAT = "All";

const grid = document.getElementById("menuGrid");
const filters = document.getElementById("menuFilters");

const modal = document.getElementById("productModal");
const modalClose = document.getElementById("modalClose");
const modalImg = document.getElementById("modalImg");
const modalTitle = document.getElementById("modalTitle");
const modalPrice = document.getElementById("modalPrice");
const modalCategory = document.getElementById("modalCategory");
const modalDesc = document.getElementById("modalDesc");
const modalTags = document.getElementById("modalTags");

// ------- helpers -------
function escapeHtml(str) {
  return String(str ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function moneyTRY(v) {
  const n = Number(v);
  if (Number.isFinite(n)) return `${n.toFixed(1)} TL`;
  return "";
}

function normalizeImagePath(image) {
  const s = String(image ?? "").trim();
  if (!s) return "/static/images/placeholder.jpg";

  // if already absolute url
  if (s.startsWith("http://") || s.startsWith("https://")) return s;

  // if relative path coming without leading slash
  if (!s.startsWith("/")) return `/${s}`;

  return s;
}

function getFilteredProducts() {
  if (ACTIVE_CAT === "All") return ALL_PRODUCTS;
  return ALL_PRODUCTS.filter((p) => (p.category || "") === ACTIVE_CAT);
}

// ------- render -------
function renderGrid() {
  const items = getFilteredProducts();

  if (!items.length) {
    grid.innerHTML = `<div style="color:#666; font-weight:600;">No products yet. Please add products from Admin Panel.</div>`;
    return;
  }

  grid.innerHTML = items
    .map((p) => {
      const imgSrc = normalizeImagePath(p.image);
      return `
      <article class="menu-card" data-id="${p.id}" style="cursor:pointer;">
        <img src="${escapeHtml(imgSrc)}" alt="${escapeHtml(p.name)}" loading="lazy">
        <div class="card-info">
          <h3>${escapeHtml(p.name)}</h3>
          <div style="color:#666; font-weight:600; margin-top:4px;">${escapeHtml(p.category || "")}</div>
          <span class="price">${escapeHtml(moneyTRY(p.price))}</span>
        </div>
      </article>
    `;
    })
    .join("");

  // click handlers
  document.querySelectorAll(".menu-card").forEach((card) => {
    card.addEventListener("click", () => {
      const id = Number(card.getAttribute("data-id"));
      const product = ALL_PRODUCTS.find((x) => Number(x.id) === id);
      if (product) openModal(product);
    });
  });
}

// ------- modal -------
function openModal(p) {
  const imgSrc = normalizeImagePath(p.image);

  modalImg.src = imgSrc;
  modalImg.alt = p.name || "Product";

  modalTitle.textContent = p.name || "";
  modalPrice.textContent = moneyTRY(p.price);
  modalCategory.textContent = p.category || "";
  modalDesc.textContent = p.description || "No description provided.";

  modalTags.innerHTML = "";
  const labels = Array.isArray(p.labels) ? p.labels : [];
  if (labels.length) {
    modalTags.innerHTML = labels
      .map((l) => `<span class="modal-tag">${escapeHtml(l)}</span>`)
      .join("");
  } else {
    modalTags.innerHTML = `<span class="modal-tag">No labels</span>`;
  }

  // ✅ "Open product page" gibi link burada yok -> tamamen kaldırdık
  modal.style.display = "flex";
}

function closeModal() {
  modal.style.display = "none";
}

modalClose?.addEventListener("click", closeModal);

modal?.addEventListener("click", (e) => {
  // click outside modal-card closes
  if (e.target === modal) closeModal();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});

// ------- filters -------
filters?.addEventListener("click", (e) => {
  const btn = e.target.closest(".filter-btn");
  if (!btn) return;

  ACTIVE_CAT = btn.getAttribute("data-cat") || "All";

  document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");

  renderGrid();
});

// ------- load -------
async function loadProducts() {
  try {
    // cache busting: admin ekledikten sonra menü refreshleyince kesin güncellensin
    const res = await fetch(`/api/products?ts=${Date.now()}`);
    if (!res.ok) {
      grid.innerHTML = `<div style="color:#b00020; font-weight:700;">Failed to load products (API error).</div>`;
      return;
    }
    ALL_PRODUCTS = await res.json();
    renderGrid();
  } catch (err) {
    grid.innerHTML = `<div style="color:#b00020; font-weight:700;">Failed to load products (Network error).</div>`;
  }
}

loadProducts();
