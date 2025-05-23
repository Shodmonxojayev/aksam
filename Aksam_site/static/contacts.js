document.addEventListener("DOMContentLoaded", function() {
    const phoneInputs = document.querySelectorAll("input[type='tel']");
    
    phoneInputs.forEach(input => {
        input.addEventListener("focus", function() {
            if (!input.value.startsWith("+998")) {
                input.value = "+998 ";
            }
        });
    });

    document.getElementById("zayavka-form").addEventListener("submit", function(event) {
        event.preventDefault();
        alert("Ваша заявка была отправлена");
    });
});
