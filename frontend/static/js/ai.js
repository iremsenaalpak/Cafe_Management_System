async function recommend() {
  const input = document.getElementById("aiPrompt");
  const out = document.getElementById("aiResult");
  if (!input || !out) return;

  const msg = (input.value || "").trim();
  if (!msg) {
    out.innerHTML = `<div class="ai-hint">Please type something (e.g. “vegan cold drink”, “no milk”, “fruit allergy”).</div>`;
    return;
  }

  out.innerHTML = `<div class="ai-hint">Preparing recommendations...</div>`;

  try {
    const res = await fetch("/api/ai-suggest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    const data = await res.json();

    if (!res.ok) {
      out.innerHTML = `<div class="ai-hint">Error: ${data.error || "Request failed"}</div>`;
      return;
    }

    const groups = ["coffee", "tea", "cold", "sweet"];
    const titleMap = {
      coffee: "Coffee",
      tea: "Tea",
      cold: "Cold Drinks",
      sweet: "Desserts"
    };

    const rec = data.recommendations || {};
    let total = 0;
    for (const g of groups) total += (rec[g]?.length || 0);

    if (!total) {
      out.innerHTML = `<div class="ai-hint">${data.info_message || "No matching items found."}</div>`;
      return;
    }

    let html = "";
    for (const g of groups) {
      const items = rec[g] || [];
      if (!items.length) continue;

      html += `<div class="ai-group">
        <div class="ai-group-title">${titleMap[g] || g}</div>`;

      for (const it of items) {
        const labels = it.labels || [];
        html += `
          <div class="ai-item">
            ${it.image ? `<img class="ai-img" src="${it.image}" alt="${it.name}">` : ""}
            <div class="ai-info">
              <div class="ai-top">
                <div class="ai-name">${it.name || "Recommendation"}</div>
                ${it.price ? `<div class="ai-price">${Math.round(it.price)} TL</div>` : ""}
              </div>

              ${labels.length ? `
                <div class="ai-tags">
                  ${labels.map(l => `<span class="ai-tag">${l}</span>`).join("")}
                </div>` : ""
              }
            </div>
          </div>`;
      }

      html += `</div>`;
    }

    out.innerHTML = html;

  } catch (e) {
    out.innerHTML = `<div class="ai-hint">Could not connect to the server.</div>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("aiBtn")?.addEventListener("click", recommend);
  document.getElementById("aiPrompt")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") recommend();
  });
});
