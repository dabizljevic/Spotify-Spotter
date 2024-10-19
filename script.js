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