console.log("Cafe script aktif.");

function filterSelection(category) {
    var elements = document.getElementsByClassName("menu-card");
    
    // 1. Tüm kartları kontrol et
    for (var i = 0; i < elements.length; i++) {
        // Eğer "all" seçildiyse hepsini göster
        if (category == "all") {
            elements[i].style.display = "block";
        } else {
            // 2. Kartın sınıfında seçilen kategori var mı?
            if (elements[i].classList.contains(category)) {
                elements[i].style.display = "block"; // Varsa göster
            } else {
                elements[i].style.display = "none";  // Yoksa gizle
            }
        }
    }

  
}