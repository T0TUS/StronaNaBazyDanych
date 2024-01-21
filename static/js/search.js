function getSuggestions() {
    var query = document.getElementById('searchInput').value;

    fetch(`/get_suggestions?query=${query}`)
        .then(response => response.json())
        .then(data => {
            displaySuggestions(data);
        });
}

function displaySuggestions(suggestions) {
    var suggestionList = document.getElementById('suggestionList');
    suggestionList.innerHTML = '';

    var searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = ''; // Wyczyszczenie poprzednich wyników

    if (suggestions.length === 0) {
        suggestionList.innerHTML = '<li>No suggestions found</li>';
        return;
    }

    suggestions.forEach(suggestion => {
        var li = document.createElement('li');
        li.textContent = `${suggestion[0]} - ${suggestion[1]} - ${suggestion[2]}`;
        li.addEventListener('click', function() {
            document.getElementById('searchInput').value = li.textContent;
            suggestionList.innerHTML = '';
        });
        suggestionList.appendChild(li);

        // Dodaj wyniki do sekcji searchResults
        var resultDiv = document.createElement('div');
        resultDiv.textContent = `${suggestion[0]} - ${suggestion[1]} - ${suggestion[2]}`;
        searchResults.appendChild(resultDiv);
    });
}

document.addEventListener('click', function(event) {
    var suggestionList = document.getElementById('suggestionList');
    if (!event.target.closest('.search-container')) {
        suggestionList.innerHTML = '';
    }
});
