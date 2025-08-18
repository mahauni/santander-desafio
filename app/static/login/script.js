const form = document.getElementById("loginForm");
const email = document.getElementById("email");
const password = document.getElementById("password");
const emailError = document.getElementById("emailError");
const pwError = document.getElementById("pwError");
const loginStatus = document.getElementById("status");

function validateEmailValue(v) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
}

const postData = {
  email: email.value,
  password: password.value,
};

form.addEventListener("submit", (e) => {
  e.preventDefault();
  emailError.style.display = "none";
  pwError.style.display = "none";
  loginStatus.textContent = "";

  let ok = true;
  if (!email.value || !validateEmailValue(email.value)) {
    emailError.style.display = "";
    emailError.textContent = "Please enter a valid email address.";
    ok = false;
  }
  if (!password.value || password.value.length < 6) {
    pwError.style.display = "";
    pwError.textContent = "Password must be at least 6 characters.";
    ok = false;
  }

  if (!ok) return;

  loginStatus.className = "";
  loginStatus.textContent = "Signing in...";

  setTimeout(() => {
    console.log("no timeout");
    $("#loginSubmit").on("click", function () {
      console.log("no click");
      $.ajax({
        url: "login",
        type: "POST",
        data: postData,
        success: function (response) {
          console.log("on success");
          loginStatus.className = "success";
          loginStatus.textContent =
            "Signed in successfully (demo). Redirecting...";
          window.location = response;
        },
        error: function (_xhr) {
          loginStatus.className = "error";
          loginStatus.textContent = "Invalid credentials (demo).";
          loginStatus.style.color =
            getComputedStyle(document.documentElement).getPropertyValue(
              "--danger",
            ) || "#ef4444";
        },
      });
    });
  }, 900);
});

email.addEventListener("blur", () => {
  if (email.value && !validateEmailValue(email.value)) {
    emailError.style.display = "";
    emailError.textContent = "Email looks invalid.";
  } else {
    emailError.style.display = "none";
  }
});
password.addEventListener("blur", () => {
  if (password.value && password.value.length < 6) {
    pwError.style.display = "";
    pwError.textContent = "Password too short.";
  } else {
    pwError.style.display = "none";
  }
});
