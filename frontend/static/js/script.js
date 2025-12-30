document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".menu-card");

  function applyFilter(filter) {
    cards.forEach(card => {
      const cat = card.dataset.category; // coffee / tea / cold / sweet
      if (filter === "all" || cat === filter) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  }

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      applyFilter(btn.dataset.filter);
    });
  });

  // default
  applyFilter("all");
});

window.openProductModal = function(p) {
  const modal = document.getElementById("productModal");
  if(!modal) return;
  const closeBtn = document.getElementById("modalClose");

  // Helper for image url
  const getImg = (obj) => {
      if(obj.image && obj.image.startsWith("/static/")) return obj.image;
      if(obj.image) return `/static/images/${obj.image}`;
      return "/static/images/placeholder.jpg";
  };

  document.getElementById("modalImg").src = getImg(p);
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
};