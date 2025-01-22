 // Profil Menüsü Aç/Kapat
 function toggleDropdown() {
    const menu = document.getElementById('profileMenu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

// Sürüklenebilir Panel
const panel = document.getElementById("layerPanel");
let isDragging = false;
let offsetX, offsetY;

panel.addEventListener("mousedown", (e) => {
    isDragging = true;
    offsetX = e.clientX - panel.offsetLeft;
    offsetY = e.clientY - panel.offsetTop;
    panel.style.cursor = "grabbing";
});

document.addEventListener("mousemove", (e) => {
    if (isDragging) {
        panel.style.left = e.clientX - offsetX + "px";
        panel.style.top = e.clientY - offsetY + "px";
    }
});

document.addEventListener("mouseup", () => {
    if (isDragging) {
        isDragging = false;
        panel.style.cursor = "grab";

        // Snap Logic: Yalnızca sol ve sağa yapışma
        const threshold = 100; // Snap Eşiği
        const windowWidth = window.innerWidth;

        // Sol tarafa ve sağ tarafa yapışma
        if (panel.offsetLeft < threshold) {
            panel.style.left = "0px"; // Sol tarafa yapış
        } else if (windowWidth - (panel.offsetLeft + panel.offsetWidth) < threshold) {
            panel.style.left = windowWidth - panel.offsetWidth + "px"; // Sağ tarafa yapış
        }

        // Navbar'ın altına hizalama
        const navbarHeight = document.querySelector(".navbar").offsetHeight;
        panel.style.top = navbarHeight + "px"; // Panel navbar'ın altına hizalanacak

        // Panelin yüksekliğini sınırlama
        const windowHeight = window.innerHeight;
        if (panel.offsetTop + panel.offsetHeight > windowHeight) {
            panel.style.height = windowHeight - panel.offsetTop - 20 + "px"; // Alt kısmı ekranda tutmak için
        }
    }
});