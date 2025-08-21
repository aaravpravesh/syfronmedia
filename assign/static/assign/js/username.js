const usernameInput = document.getElementById("username");
  const feedback = document.getElementById("username-feedback");

  usernameInput.addEventListener("keyup", function () {
    const username = usernameInput.value;

    if (username.length > 2) {  // check only after 3+ chars
      fetch(`/check-username/?username=${username}`)
        .then(response => response.json())
        .then(data => {
          if (data.is_taken) {
            feedback.style.display = "block";
            feedback.textContent = "❌ Username is already taken";
            feedback.style.color = "red";
            usernameInput.classList.add("is-invalid");
          } else {
            feedback.style.display = "block";
            feedback.textContent = "✅ Username is available";
            feedback.style.color = "green";
            usernameInput.classList.remove("is-invalid");
            usernameInput.classList.add("is-valid");
          }
        });
    } else {
      feedback.style.display = "none";
      usernameInput.classList.remove("is-valid", "is-invalid");
    }
  });