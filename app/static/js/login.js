const loginForm = document.querySelector(".login-form");
const registerForm = document.querySelector(".register-form");
const wrapper = document.querySelector(".wrapper");
const loginTitle = document.querySelector(".title-login");
const registerTitle = document.querySelector(".title-register");
const signUpBtn = document.querySelector("#SignUpBtn");
const signInBtn = document.querySelector("#SignInBtn");

// -----------------------------
// Login / Register Toggle
// -----------------------------
function loginFunction() {
    loginForm.style.left = "50%";
    loginForm.style.opacity = 1;
    registerForm.style.left = "150%";
    registerForm.style.opacity = 0;
    wrapper.style.height = "500px";
    loginTitle.style.top = "50%";
    loginTitle.style.opacity = 1;
    registerTitle.style.top = "50px";
    registerTitle.style.opacity = 0;
}

function registerFunction() {
    loginForm.style.left = "-50%";
    loginForm.style.opacity = 0;
    registerForm.style.left = "50%";
    registerForm.style.opacity = 1;
    wrapper.style.height = "680px";
    loginTitle.style.top = "-60px";
    loginTitle.style.opacity = 0;
    registerTitle.style.top = "50%";
    registerTitle.style.opacity = 1;
}

signUpBtn?.addEventListener("click", registerFunction);
signInBtn?.addEventListener("click", loginFunction);

// -----------------------------
// Flash Messages (auto dismiss)
// -----------------------------
window.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll(".flash-message");

    toasts.forEach((toast, i) => {
        toast.querySelector(".flash-close")?.addEventListener("click", () => {
            toast.classList.add("hide");
            setTimeout(() => toast.remove(), 280);
        });

        setTimeout(() => {
            if (!toast.classList.contains("hide")) {
                toast.classList.add("hide");
                setTimeout(() => toast.remove(), 280);
            }
        }, 3000 + i * 120);
    });
});

// -----------------------------
// Password Field Icons
// -----------------------------
function initPasswordToggles() {
    document.querySelectorAll(".password-toggle").forEach(container => {
        const input = container.querySelector(".input-field");
        const lockIcon = container.querySelector(".lock-icon");
        const eyeIcon = container.querySelector(".eye-icon");

        function updateIcons() {
            if (input.value.length > 0) {
                if (lockIcon) lockIcon.style.display = "none";
                if (eyeIcon) eyeIcon.style.display = "block";
            } else {
                if (lockIcon) lockIcon.style.display = "block";
                if (eyeIcon) eyeIcon.style.display = "none";
            }
        }

        // Toggle visibility
        if (eyeIcon) { // Check if the eyeIcon element exists
            eyeIcon.addEventListener("click", () => {
                if (input.type === "password") {
                    input.type = "text";
                    eyeIcon.classList.remove("bx-hide");
                    eyeIcon.classList.add("bx-show");
                } else {
                    input.type = "password";
                    eyeIcon.classList.remove("bx-show");
                    eyeIcon.classList.add("bx-hide");
                }
                input.focus();
                const val = input.value;
                input.setSelectionRange(val.length, val.length);
            });
        }
        
        input.addEventListener("input", updateIcons);
        updateIcons(); // Run on load
    });
}

document.addEventListener("DOMContentLoaded", initPasswordToggles);