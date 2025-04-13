async function login(e) {
  e.preventDefault();
  const partner1 = document.getElementById("partner1").value.trim();
  const password = document.getElementById("password").value.trim();

  const response = await fetch("http://localhost:8000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ partner1, password }),
  });

  const result = await response.json();
  const messageElement = document.getElementById("message");

  if (response.ok) {
    const partner2 = result.partner2 || "Anonymous";
    localStorage.setItem("coupleNames", `${partner1} ❤️ ${partner2}`);
    window.location.href = "modules.html";
  } else {
    messageElement.textContent =
      result.detail || "fix the login then I will fix you 😢🥲💕";
    messageElement.style.color = "dark-pink";
  }
}
