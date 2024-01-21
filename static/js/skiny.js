function redirectToDetails(skinName) {
    window.location.href = `/skin/${encodeURIComponent(skinName.replace(/\s+/g, ' '))}`;
}

// W odpowiednim miejscu na stronie
var skinImageContainer = document.getElementById('skinImageContainer');
if (skinImageContainer) {
    var skinName = "AWP | Asiimov (Battle-Scarred)";  // Tutaj ustaw nazwę skórki
    var image = new Image();
    image.src = `/skin/${encodeURIComponent(skinName.replace(/\s+/g, ' '))}`;

    // Dodaj obrazek do kontenera po załadowaniu
    image.onload = function() {
        skinImageContainer.appendChild(image);
    };
}