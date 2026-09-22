document.addEventListener("DOMContentLoaded", function () {

    const menuBurger = document.getElementById("menuBurger");
    const navMenu = document.getElementById("navMenu");

    if (!menuBurger || !navMenu) {
        return;
    }

    menuBurger.addEventListener("click", function () {

        navMenu.classList.toggle("active");

        const ouvert = navMenu.classList.contains("active");

        menuBurger.setAttribute("aria-expanded", ouvert);

        if (ouvert) {
            menuBurger.innerHTML = '<i class="fa-solid fa-xmark"></i>';
        } else {
            menuBurger.innerHTML = '<i class="fa-solid fa-bars"></i>';
        }

    });


    /* Fermer le menu après avoir cliqué sur un lien */

    navMenu.querySelectorAll("a").forEach(function (lien) {

        lien.addEventListener("click", function () {

            navMenu.classList.remove("active");

            menuBurger.setAttribute("aria-expanded", "false");

            menuBurger.innerHTML =
                '<i class="fa-solid fa-bars"></i>';

        });

    });

});



