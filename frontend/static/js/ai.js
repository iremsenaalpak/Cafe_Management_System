document.addEventListener("DOMContentLoaded", () => {
    const out = document.getElementById("aiResult");
    
    // Botun ilk selamlaması (Otomatik başlar)
    if (out) {
        addMessage("bot", "Hello! How are you today? 😊");
        addMessage("bot", "What are you craving today: <b>Coffee, Tea, Cold Drinks, or Desserts?</b>");
    }

    document.getElementById("aiBtn")?.addEventListener("click", recommend);
    document.getElementById("aiPrompt")?.addEventListener("keydown", (e) => {
        if (e.key === "Enter") recommend();
    });
});

// Yeni mesaj balonu ekleme fonksiyonu (Tasarımı burası yapar)
function addMessage(sender, text) {
    const out = document.getElementById("aiResult");
    
    // Tasarım ayarları: Bot gri ve solda, kullanıcı koyu yeşil ve sağda
    const sideStyle = sender === "user" 
        ? "align-self: flex-end; background: #2d433d; color: white; border-radius: 15px 15px 0 15px;" 
        : "align-self: flex-start; background: #f0f0f0; color: #333; border-radius: 15px 15px 15px 0;";
    
    const bubble = `
        <div class="ai-bubble" style="${sideStyle} padding: 10px 15px; max-width: 80%; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 5px;">
            ${text}
        </div>
    `;
    
    out.innerHTML += bubble;
    out.scrollTop = out.scrollHeight; // Her yeni mesajda otomatik aşağı kaydır
}

async function recommend() {
    const input = document.getElementById("aiPrompt");
    const msg = input.value.trim();
    if (!msg) return;

    // Kullanıcının mesajını ekle
    addMessage("user", msg);
    input.value = "";

    try {
        const res = await fetch("http://127.0.0.1:5000/api/ai-assistant", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();

        // Botun cevabını ekle
        if (data.recommendations) {
            addMessage("bot", "I found some great options for you! Feel free to check the menu cards on the screen.");
        } else {
            addMessage("bot", "I'm not sure I found that. Could you try asking for something else?");
        }
    } catch (e) {
        addMessage("bot", "Sorry, I'm having trouble connecting to the server right now.");
    }
}