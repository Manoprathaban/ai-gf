document.getElementById("simulateBtn").addEventListener("click", async () => {
  const scenario = document.getElementById("scenario").value.trim();
  const mode = document.getElementById("mode").value;

  if (!scenario) {
    alert("Please enter a scenario.");
    return;
  }

  const responseElement = document.getElementById("response");
  responseElement.textContent = "Generating your date...";

  try {
    const res = await fetch("http://localhost:8000/date/simulate-date", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ scenario, mode }),
    });

    const data = await res.json();

    if (data.response) {
      responseElement.textContent = data.response;
    } else {
      responseElement.textContent = "Error: " + (data.error || "Unknown error");
    }
  } catch (error) {
    responseElement.textContent = "An error occurred. Please try again.";
    console.error("Fetch error:", error);
  }
});
