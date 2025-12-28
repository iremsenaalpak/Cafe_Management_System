/**
 * Recommendation Engine Frontend
 * Handles the interaction between the user input and the AI Assistant API.
 */
async function recommend() {
    const input = document.getElementById("aiPrompt");
    const out = document.getElementById("aiResult");
    
    // Check if required DOM elements exist
    if (!input || !out) return;

    const msg = (input.value || "").trim();
    if (!msg) {
        out.innerHTML = `<div class="ai-hint">Please type something (e.g., "vegan cold drink", "no milk", "fruit allergy").</div>`;
        return;
    }

    // Show loading state to the user
    out.innerHTML = `<div class="ai-hint">AI is analyzing your request and preparing recommendations...</div>`;

    try {
        // Send request to the Flask AI Assistant Endpoint
        // Note: Using absolute URL to ensure connection to port 5000
        const res = await fetch("http://127.0.0.1:5000/api/ai-assistant", {
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
            coffee: "Coffee Specials",
            tea: "Tea Selection",
            cold: "Cold Beverages",
            sweet: "Delicious Desserts"
        };

        const rec = data.recommendations || {};
        
        // Calculate total recommendations found
        let total = 0;
        groups.forEach(g => {
            total += (rec[g]?.length || 0);
        });

        // Handle case where no items match the AI's criteria
        if (total === 0) {
            out.innerHTML = `<div class="ai-hint">No matching items found for your request. Try different keywords!</div>`;
            return;
        }

        // Build HTML for recommendation groups
        let html = "";
        for (const g of groups) {
            const items = rec[g] || [];
            if (!items.length) continue;

            html += `<div class="ai-group">
                <div class="ai-group-title">${titleMap[g] || g}</div>`;

            for (const it of items) {
                const labels = it.labels || [];
                
                // Format image path correctly based on project structure
                const imageSrc = it.image ? `/static/images/uploads/${it.image}` : "/static/images/placeholder.jpg";

                html += `
                  <div class="ai-item">
                    <img class="ai-img" src="${imageSrc}" alt="${it.name || 'Product'}">
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
        console.error("Connection Error:", e);
        out.innerHTML = `<div class="ai-hint">Could not connect to the AI server. Please make sure the backend is running on port 5000.</div>`;
    }
}

/**
 * Event Listeners for Assistant UI
 */
document.addEventListener("DOMContentLoaded", () => {
    const aiBtn = document.getElementById("aiBtn");
    const aiPrompt = document.getElementById("aiPrompt");

    // Trigger recommendation on button click
    aiBtn?.addEventListener("click", recommend);

    // Trigger recommendation on "Enter" key press
    aiPrompt?.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            recommend();
        }
    });
});