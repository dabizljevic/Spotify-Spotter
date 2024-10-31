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
    if (recently_played.style.display == "none") {
        recently_played.style.display = "block";
    } else {
        recently_played.style.display = "none";
    }
}

function display_top_songs_artists() {
    var time_frame = document.getElementById("time-frame").value;
    var link = document.getElementById("change-with-time-frame");
    if (time_frame == "last-4-weeks") {
        link.innerHTML = "Last Four Weeks"
        link.setAttribute("href", "/top-songs-artists?time_range=short_term");
        return false;
    }
    if (time_frame == "last-6-months") {
        link.innerHTML = "Last Six Months"
        link.setAttribute("href", "/top-songs-artists?time_range=medium_term");
        return false;
    }
    if (time_frame == "all-time") {
        link.innerHTML = "All Time!"
        link.setAttribute("href", "/top-songs-artists?time_range=long_term");
        return false;
    }
}