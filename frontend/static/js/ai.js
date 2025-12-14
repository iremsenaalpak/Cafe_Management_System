async function recommend() {
  const input = document.getElementById("aiPrompt");
  const out = document.getElementById("aiResult");
  if (!input || !out) return;

  const msg = (input.value || "").trim();
  if (!msg) {
    out.innerHTML = `<p style="margin:0;">Please type something (e.g. "recommend a diet drink").</p>`;
    return;
  }

  out.innerHTML = `<p style="margin:0;">Preparing recommendations...</p>`;

  try {
    const res = await fetch("/api/ai-suggest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    const data = await res.json();

    if (!res.ok) {
      out.innerHTML = `<p style="margin:0;">Error: ${data.error || "Request failed"}</p>`;
      return;
    }

    const rec = data.recommendations || {};
    const groups = ["coffee", "tea", "cold", "sweet"];

    let total = 0;
    for (const g of groups) total += (rec[g]?.length || 0);

    if (!total) {
      out.innerHTML = `<p style="margin:0;">${data.info_message || "No matching items found."}</p>`;
      return;
    }

    const titleMap = {
      coffee: "Coffee",
      tea: "Tea",
      cold: "Cold Drinks",
      sweet: "Desserts"
    };

    let html = "";

    for (const g of groups) {
      const items = rec[g] || [];
      if (!items.length) continue;

      html += `<div class="ai-group">
        <h4 class="ai-group-title">${titleMap[g] || g}</h4>
        <div class="ai-cards">`;

      for (const it of items) {
        const tags = [];
        if (it.vegan) tags.push("Vegan");
        if (it.low_calorie) tags.push("Low Calorie");
        if (it.sugar_free) tags.push("Sugar Free");

        html += `
          <div class="ai-item">
            ${it.img ? `<img class="ai-img" src="/static/images/${it.img}" alt="${it.name}">` : ""}
            <div class="ai-info">
              <div class="ai-top">
                <strong class="ai-name">${it.name || "Recommendation"}</strong>
                ${it.price ? `<span class="ai-price">${it.price} TL</span>` : ""}
              </div>
              ${it.desc ? `<div class="ai-desc">${it.desc}</div>` : ""}
              ${tags.length ? `<div class="ai-tags">${tags.map(t => `<span class="ai-tag">${t}</span>`).join("")}</div>` : ""}
            </div>
          </div>`;
      }

      html += `</div></div>`;
    }

    out.innerHTML = html;

  } catch (e) {
    out.innerHTML = `<p style="margin:0;">Could not connect to the server.</p>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("aiBtn")?.addEventListener("click", recommend);
  document.getElementById("aiPrompt")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") recommend();
  });
});
