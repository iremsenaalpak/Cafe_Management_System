document.addEventListener("DOMContentLoaded", () => {
  const widget = document.getElementById("chatWidget");
  const toggleBtn = document.getElementById("chatToggle");
  const closeBtn = document.getElementById("chatClose");
  const sendBtn = document.getElementById("chatSend");
  const input = document.getElementById("chatInput");
  const chatBody = document.getElementById("chatBody");

  // Toggle Widget
  function toggleChat() {
    if (widget.style.display === "none") {
      widget.style.display = "flex";
      input.focus();
    } else {
      widget.style.display = "none";
    }
  }

  toggleBtn?.addEventListener("click", toggleChat);
  closeBtn?.addEventListener("click", () => widget.style.display = "none");

  // Send Message
  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    // User Message
    addMessage("user", text);
    input.value = "";

    // Loading indicator
    const loadingId = addMessage("bot", "...");
    const loadingEl = document.getElementById(loadingId);

    try {
      const res = await fetch("/api/ai-suggest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();
      
      // Remove loading text
      if (loadingEl) loadingEl.remove();

      if (data.error) {
        addMessage("bot", "Sorry, I encountered an error.");
        return;
      }

      // Add Bot Reply
      if (data.reply) {
        addMessage("bot", data.reply);
      }

      // Add Recommendations
      if (data.recommendations) {
        renderRecommendations(data.recommendations);
      }

    } catch (err) {
      if (loadingEl) loadingEl.remove();
      addMessage("bot", "Could not reach the server.");
    }
  }

  sendBtn?.addEventListener("click", sendMessage);
  input?.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // Helpers
  function addMessage(sender, text) {
    const id = "msg-" + Date.now();
    const div = document.createElement("div");
    div.className = `chat-msg ${sender}`;
    div.id = id;
    
    // Icon for bot
    let iconHtml = "";
    if (sender === "bot") {
      iconHtml = `<img src="/static/images/robot.png" alt="AI">`;
    }

    div.innerHTML = `
      ${iconHtml}
      <div class="msg-txt">${text}</div>
    `;
    
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
    return id;
  }

  function renderRecommendations(recs) {
    // Flatten recommendations
    const all = [];
    if (recs.coffee) all.push(...recs.coffee);
    if (recs.tea) all.push(...recs.tea);
    if (recs.cold) all.push(...recs.cold);
    if (recs.sweet) all.push(...recs.sweet);

    if (all.length === 0) return;

    const div = document.createElement("div");
    div.className = "chat-recs";
    div.innerHTML = `<div class="rec-title">RECOMMENDED:</div>`;
    
    all.forEach(p => {
        const item = document.createElement("div");
        item.className = "rec-item";
        // Make clickable
        item.onclick = () => {
            if (window.openProductModal) {
                window.openProductModal(p);
            }
        };
        
        item.innerHTML = `
            <img src="${p.image || '/static/images/placeholder.jpg'}" alt="${p.name}">
            <div class="rec-info">
                <div class="rec-name">${p.name}</div>
                <div class="rec-price">${p.price} TL</div>
                <div class="rec-tags">
                   ${(p.labels || []).map(l => `<span>${l}</span>`).join("")} 
                </div>
            </div>
        `;
        div.appendChild(item);
    });

    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});
