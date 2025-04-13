async function signup(e) {
  e.preventDefault();

  const partner1 = document.getElementById("newPartner1").value.trim();
  const partner2 =
    document.getElementById("newPartner2").value.trim() || "Anonymous";
  const password = document.getElementById("newPassword").value.trim();

  const response = await fetch("http://localhost:8000/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ partner1, partner2, password }),
  });

  const result = await response.json();

  const msg = document.getElementById("signupMessage");
  if (response.ok) {
    msg.textContent = "Signup successful 💖 Redirecting to login...";
    msg.style.color = "green";
    setTimeout(() => {
      window.location.href = "index.html";
    }, 2000);
  } else {
    msg.textContent = result.detail || "fix the login then i will fix you ❤️";
    msg.style.color = "red";
  }
}
