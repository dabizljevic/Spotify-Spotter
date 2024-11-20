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

function handleArtistsChange() {
    var selected = document.getElementById('artists').value;
    var short_term = document.getElementById("stArtists");
    var medium_term = document.getElementById("mtArtists");
    var long_term = document.getElementById("ltArtists");
    if (selected == "short") {
        short_term.style.display = "block";
        medium_term.style.display = "none";
        long_term.style.display = "none";
    }
    if (selected == "medium") {
        short_term.style.display = "none";
        medium_term.style.display = "block";
        long_term.style.display = "none";
    }
    if (selected == "long") {
        short_term.style.display = "none";
        medium_term.style.display = "none";
        long_term.style.display = "block";
    }
}

function handleTracksChange() {
    var selected = document.getElementById('tracks').value;
    var short_term = document.getElementById("stTracks");
    var medium_term = document.getElementById("mtTracks");
    var long_term = document.getElementById("ltTracks");
    if (selected == "short") {
        short_term.style.display = "block";
        medium_term.style.display = "none";
        long_term.style.display = "none";
    }
    if (selected == "medium") {
        short_term.style.display = "none";
        medium_term.style.display = "block";
        long_term.style.display = "none";
    }
    if (selected == "long") {
        short_term.style.display = "none";
        medium_term.style.display = "none";
        long_term.style.display = "block";
    }
}

function handleGenresChange() {
    var selected = document.getElementById('genres').value;
    var short_term = document.getElementById("stGenres");
    var medium_term = document.getElementById("mtGenres");
    var long_term = document.getElementById("ltGenres");
    if (selected == "short") {
        short_term.style.display = "block";
        medium_term.style.display = "none";
        long_term.style.display = "none";
    }
    if (selected == "medium") {
        short_term.style.display = "none";
        medium_term.style.display = "block";
        long_term.style.display = "none";
    }
    if (selected == "long") {
        short_term.style.display = "none";
        medium_term.style.display = "none";
        long_term.style.display = "block";
    }
}

function handlePlaylistChange() {
    var selected = document.getElementById('playlists').value;
    var top = document.getElementById("topTracksPlaylist");
    var similar = document.getElementById("similarArtistsPlaylist");
    var mood = document.getElementById("moodBasedPlaylist");
    var recent = document.getElementById("recentlyPlayedPlaylist");

    if (selected == "top_tracks") {
        top.style.display = "block";
        similar.style.display = "none";
        mood.style.display = "none";
        recent.style.display = "none";
    }
    if (selected == "similar_artists") {
        top.style.display = "none";
        similar.style.display = "block";
        mood.style.display = "none";
        recent.style.display = "none";
    }
    if (selected == "mood_based") {
        top.style.display = "none";
        similar.style.display = "none";
        mood.style.display = "block";
        recent.style.display = "none";
    }
    if (selected == "recently_played") {
        top.style.display = "none";
        similar.style.display = "none";
        mood.style.display = "none";
        recent.style.display = "block";
    }
}
