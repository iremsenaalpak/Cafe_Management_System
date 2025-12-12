function setActiveButton(category) {
  const btns = document.querySelectorAll(".filter-btn");
  btns.forEach(b => b.classList.remove("active"));

  // onclick içinde ilgili category geçen butonu aktif yap
  const clicked = Array.from(btns).find(b => (b.getAttribute("onclick") || "").includes("'" + category + "'"));
  if (clicked) clicked.classList.add("active");
}

function filterSelection(category) {
  const cards = document.querySelectorAll(".filter-item");

  cards.forEach(card => {
    const cat = card.getAttribute("data-category");
    card.style.display = (category === "all" || cat === category) ? "block" : "none";
  });

  setActiveButton(category);
}

// page load: show all (only if menu page has cards)
document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector(".filter-item")) {
    filterSelection("all");
  }
});

/* -------------------------
   AI Assistant (Home Page)
------------------------- */
function escapeHtml(str) {
  return (str || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderCategory(title, items) {
  if (!items || items.length === 0) return "";

  const cards = items.map(item => {
    const imgHtml = item.img
      ? `<img src="/static/images/${encodeURIComponent(item.img)}" alt="${escapeHtml(item.name)}">`
      : "";

    const badges = [
      item.vegan ? `<span class="badge">Vegan</span>` : "",
      item.low_calorie ? `<span class="badge">Low Calorie</span>` : "",
      item.sugar_free ? `<span class="badge">Sugar Free</span>` : "",
    ].join("");

    const ingredients = (item.ingredients || []).join(", ");

    return `
      <div class="menu-card">
        ${imgHtml}
        <h3>${escapeHtml(item.name)}</h3>
        ${item.desc ? `<p>${escapeHtml(item.desc)}</p>` : ""}
        <p><b>Ingredients:</b> ${escapeHtml(ingredients)}</p>
        <div>${badges}</div>
        ${item.price != null ? `<span class="price">${item.price} TL</span>` : ""}
      </div>
    `;
  }).join("");

  return `
    <h3 style="margin:18px 0 10px; color: var(--main-green);">${title}</h3>
    <div class="menu-grid">${cards}</div>
  `;
}

async function askAiRecommend() {
  const input = document.getElementById("aiInput");
  const btn = document.getElementById("aiBtn");
  const info = document.getElementById("aiInfo");
  const results = document.getElementById("aiResults");

  if (!input || !btn || !info || !results) return;

  const message = (input.value || "").trim();
  if (!message) {
    info.textContent = "Please type a message (e.g. 'recommend me something vegan').";
    return;
  }

  info.textContent = "Thinking...";
  results.innerHTML = "";
  btn.disabled = true;

  try {
    const res = await fetch("/api/ai-suggest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();

    if (!res.ok) {
      info.textContent = data?.error || "Request failed.";
      return;
    }

    info.textContent = data.info_message || "";

    const rec = data.recommendations || {};
    const html =
      renderCategory("Coffee", rec.coffee) +
      renderCategory("Tea", rec.tea) +
      renderCategory("Sweet", rec.sweet);

    results.innerHTML = html || `<p>No recommendations found.</p>`;
  } catch (e) {
    info.textContent = "Network error. Please try again.";
  } finally {
    btn.disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("aiBtn");
  const input = document.getElementById("aiInput");

  if (btn) btn.addEventListener("click", askAiRecommend);
  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") askAiRecommend();
    });
  }
});

