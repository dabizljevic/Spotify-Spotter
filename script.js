// script.js
const menuButton = document.getElementById('menuButton');
const navigationMenu = document.getElementById('navigationMenu');

menuButton.addEventListener('click', () => {
    navigationMenu.classList.toggle('show');
});