document.addEventListener("DOMContentLoaded", function () {
    const searchBar = document.getElementById("search-bar");
    const suggestionsList = document.getElementById("suggestions-list");

    searchBar.addEventListener("input", function () {
        const inputText = searchBar.value.toLowerCase();

        // Here you can replace this array with data from your database
        const suggestions = ["Option 1", "Option 2", "Option 3", "Option 4"];

        // Clear previous suggestions
        suggestionsList.innerHTML = "";

        // Filter and display matching suggestions
        const filteredSuggestions = suggestions.filter(function (suggestion) {
            return suggestion.toLowerCase().includes(inputText);
        });

        filteredSuggestions.forEach(function (suggestion) {
            const li = document.createElement("li");
            li.textContent = suggestion;
            suggestionsList.appendChild(li);
        });

        // Display or hide suggestions list based on input
        if (inputText.length > 0 && filteredSuggestions.length > 0) {
            suggestionsList.style.display = "block";
        } else {
            suggestionsList.style.display = "none";
        }
    });

    // Handle suggestion click
    suggestionsList.addEventListener("click", function (event) {
        if (event.target.tagName === "LI") {
            searchBar.value = event.target.textContent;
            suggestionsList.style.display = "none";
        }
    });

    // Hide suggestions when clicking outside the search container
    document.addEventListener("click", function (event) {
        if (!event.target.closest(".search-container")) {
            suggestionsList.style.display = "none";
        }
    });
});
