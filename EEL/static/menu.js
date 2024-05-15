document.addEventListener('DOMContentLoaded', function() {
    var hamburger = document.querySelector('.hamburger');
    var menu = document.querySelector('nav ul');

    hamburger.addEventListener('click', function() {
        if (menu.style.maxHeight) {
            menu.style.maxHeight = null;
        } else {
            menu.style.maxHeight = menu.scrollHeight + "px";
        }
    });
});