  const password = document.getElementById("password");
  const password2 = document.getElementById("password2");
  const strengthBar = document.getElementById("strength-bar");
  const strengthMessage = document.getElementById("strength-message");
  const matchMessage = document.getElementById("password-message");
  const submitBtn = document.getElementById("submit-btn");

  // ✅ Password strength checker
  function checkStrength(pwd) {
    let strength = 0;
    if (pwd.length >= 6) strength++;
    if (/[A-Z]/.test(pwd)) strength++;
    if (/[0-9]/.test(pwd)) strength++;
    if (/[^A-Za-z0-9]/.test(pwd)) strength++;

    const strengths = [
      {text: "Weak", color: "bg-danger", width: "25%"},
      {text: "Fair", color: "bg-warning", width: "50%"},
      {text: "Good", color: "bg-info", width: "75%"},
      {text: "Strong", color: "bg-success", width: "100%"},
    ];

    if (strength > 0) {
      const s = strengths[strength-1];
      strengthBar.style.width = s.width;
      strengthBar.className = "progress-bar " + s.color;
      strengthMessage.textContent = "Strength: " + s.text;
    } else {
      strengthBar.style.width = "0%";
      strengthMessage.textContent = "";
    }
  }

  // ✅ Password match check
  function checkMatch() {
    if (password.value === "" || password2.value === "") {
      matchMessage.textContent = "";
      submitBtn.disabled = true;
      return;
    }

    if (password.value === password2.value) {
      matchMessage.textContent = "✅ Passwords match";
      matchMessage.style.color = "green";
      submitBtn.disabled = false;
    } else {
      matchMessage.textContent = "❌ Passwords do not match";
      matchMessage.style.color = "red";
      submitBtn.disabled = true;
    }
  }

  password.addEventListener("input", () => {
    checkStrength(password.value);
    checkMatch();
  });
  password2.addEventListener("input", checkMatch);

  // ✅ Realtime username & email availability check
  async function checkAvailability(field, value, feedbackId, url) {
    if (!value) {
      document.getElementById(feedbackId).textContent = "";
      return;
    }
    try {
      const response = await fetch(`${url}?${field}=${value}`);
      const data = await response.json();
      const feedback = document.getElementById(feedbackId);

      if (data.exists) {
        feedback.textContent = `${field} already taken ❌`;
        feedback.style.color = "red";
        submitBtn.disabled = true;
      } else {
        feedback.textContent = `${field} available ✅`;
        feedback.style.color = "green";
      }
    } catch (error) {
      console.error("Error checking availability:", error);
    }
  }

  document.getElementById("username").addEventListener("blur", function () {
    checkAvailability("username", this.value, "username-feedback", "/check-username/");
  });

  document.getElementById("email").addEventListener("blur", function () {
    checkAvailability("email", this.value, "email-feedback", "/check-email/");
  });
