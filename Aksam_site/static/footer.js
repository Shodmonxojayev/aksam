// footer.js
document.getElementById("subscribe-btn").addEventListener("click", function() {
  let emailInput = document.getElementById("email");
  let message = document.getElementById("subscribe-message");
  let email = emailInput.value.trim();

  if (email === "") {
      message.textContent = "Iltimos, email kiriting!";
      message.style.color = "red";
      return;
  }

  let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
      message.textContent = "Email noto‘g‘ri kiritildi!";
      message.style.color = "red";
      return;
  }

  message.textContent = "Obuna bo'lganingiz uchun raxmat!";
  message.style.color = "green";
  emailInput.value = "";
});
