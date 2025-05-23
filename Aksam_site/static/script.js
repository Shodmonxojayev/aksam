document.addEventListener("DOMContentLoaded", function () {
    const burgerMenuBtn = document.getElementById("burger-menu-btn");
    const menu = document.querySelector(".menu");
    const closeBtn = document.querySelector(".close-btn");

    // Menyuni ochish
    burgerMenuBtn.addEventListener("click", function () {
        menu.style.display = "block";
    });

    // Menyuni yopish
    closeBtn.addEventListener("click", function () {
        menu.style.display = "none";
    });

    // Ekranga bosganda menyuni yopish (agar menyu ochiq bo'lsa)
    document.addEventListener("click", function (event) {
        if (!menu.contains(event.target) && event.target !== burgerMenuBtn) {
            menu.style.display = "none";
        }
    });
});
