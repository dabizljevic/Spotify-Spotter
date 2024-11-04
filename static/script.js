// script.js
var formatting = { weekday: 'long', month: 'long', day: 'numeric'};
var date = new Date();
var today = date.toLocaleDateString("en-US", formatting);
date.setDate(date.getDate() - (date.getDate() + 3) % 7);
var lastFriday = date.toLocaleDateString("en-US", formatting)
if (lastFriday == today) {
    date.setDate(date.getDate() - 7);
    lastFriday = date.toLocaleDateString("en-US", formatting);
}
date.setDate(date.getDate() - (date.getDate() + 4) % 7);
date.setDate(date.getDate() + 7);
var currentThursday = date.toLocaleDateString("en-US", formatting)
document.getElementById("today").innerHTML = today;
document.getElementById("lastFriday").innerHTML = lastFriday;
document.getElementById("currentThursday").innerHTML = currentThursday;

function display_recently_played() {
    var recently_played = document.getElementById("recently-played");
    var img = document.getElementById("dropdown_recently_played");
    if (recently_played.style.display == "none") {
        recently_played.style.display = "block";
        img.style.transform = "rotate(180deg)";
    } else {
        recently_played.style.display = "none";
        img.style.transform = "rotate(0deg)";
    }
}

function display_top_songs() {
    var top_songs = document.getElementById("top-songs");
    var img = document.getElementById("dropdown_top_songs");
    if (top_songs.style.display == "none") {
        top_songs.style.display = "block";
        img.style.transform = "rotate(180deg)";
    } else {
        top_songs.style.display = "none";
        img.style.transform = "rotate(0deg)";
    }
}


function display_top_artists() {
    var top_artists = document.getElementById("top-artists");
    var img = document.getElementById("dropdown_top_artists");
    if (top_artists.style.display == "none") {
        top_artists.style.display = "block";
        img.style.transform = "rotate(180deg)";
    } else {
        top_artists.style.display = "none";
        img.style.transform = "rotate(0deg)";
    }
}

function display_top_songs_artists() {
    var top_songs_artists = document.getElementById("top-songs-and-artists");
    var img = document.getElementById("dropdown_top_songs_artists");

    if (top_songs_artists.style.display == "none") {
        top_songs_artists.style.display = "block";
        img.style.transform = "rotate(180deg)";
    } else {
        top_songs_artists.style.display = "none";
        img.style.transform = "rotate(0deg)";
    }
}

function time_frame_changed() {
    var time_frame = document.getElementById("time-frame").value;
    if (time_frame == "short_term") {
        window.location.href = "/user?time_range=short_term";
    }
    if (time_frame == "medium_term") {
        window.location.href = "/user?time_range=medium_term";
    }
    if (time_frame == "long_term") {
        window.location.href = "/user?time_range=long_term";
    }
}

function display_top_genres() {
    var top_genres =  document.getElementById("top-genres");
    var img = document.getElementById("dropdown_top_genres");

    if (top_genres.style.display == "none") {
        top_genres.style.display = "block";
        img.style.transform = "rotate(180deg)";
    } else {
        top_genres.style.display = "none";
        img.style.transform = "rotate(0deg)";
    }

}
// async function display_top_songs_artists() {
//     const time_frame = document.getElementById('time-frame').value;
//     const display = document.getElementById('top-songs-artists-list');
    
//     display.innerHTML = "Make call to /top-song-artists with key: " + time_frame;
//     try {
//         const response = await fetch('/api/data?time_range=${time_frame}');
//         if (!response.ok) {
//             throw new Error('Response DNE');
//         }
//         const data = await response.json();
//         data.forEarch(item => {
//             const listItem = document.createElement('li');
//             listItem.textContent = '${item.name} - ${item.artist}';
//             listItem.appendChild(listItem);
//         });
//     } catch (error) {
//         console.error('Error fetching data:', error);
//         const errorItem = document.createElement('li');
//         errorItem.textContent = 'Error loading data!';
//         display.appendChild(errorItem);
//     }
// }