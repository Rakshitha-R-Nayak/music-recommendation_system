document.getElementById("song-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission
    const songName = document.getElementById("song-input").value; // Get song name from input

    // Send the song name to the backend
    const response = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ song_name: songName })
    });

    // Get the recommendations from the response
    const recommendations = await response.json();

    // Display the recommendations on the page
    const recDiv = document.getElementById("recommendations");
    recDiv.innerHTML = recommendations.map(song => `<p>${song}</p>`).join('');
});