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