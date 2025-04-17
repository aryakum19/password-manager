document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("add-password-form");
    const passwordsContainer = document.getElementById("passwords-container");
    const systemPasswordModal = document.getElementById("system-password-modal");
    const systemPasswordInput = document.getElementById("system-password");
    const confirmPasswordBtn = document.getElementById("confirm-password-btn");
    const passwordInput = document.getElementById("password");

    let revealId = null;

    function getPasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/\d/.test(password)) strength++;
        if (/[\W]/.test(password)) strength++;

        if (strength >= 5) return "Strong 🔒";
        if (strength >= 3) return "Medium 🛡️";
        return "Weak ⚠️";
    }

    passwordInput.addEventListener("input", function () {
        const val = this.value;
        document.getElementById("strength-indicator").textContent = val ? "Strength: " + getPasswordStrength(val) : "";
    });

    document.getElementById("generate-btn").addEventListener("click", function () {
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+[]{}|;:,.<>?";
        let password = "";
        for (let i = 0; i < 16; i++) {
            password += charset[Math.floor(Math.random() * charset.length)];
        }
        passwordInput.value = password;
        document.getElementById("strength-indicator").textContent = "Strength: " + getPasswordStrength(password);
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const service = document.getElementById("service").value;
        const username = document.getElementById("username").value;
        const password = passwordInput.value;

        const res = await fetch("/api/passwords", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ service, username, password }),
        });

        if (res.ok) {
            form.reset();
            loadPasswords();
        }
    });

    async function loadPasswords() {
        const res = await fetch("/api/passwords");
        const data = await res.json();
        passwordsContainer.innerHTML = "";

        for (const service in data) {
            const section = document.createElement("div");
            section.className = "section";
            const title = document.createElement("h3");
            title.textContent = service;
            section.appendChild(title);

            data[service].forEach(entry => {
                const entryDiv = document.createElement("div");
                entryDiv.className = "password-entry";

                entryDiv.innerHTML = `
                    <p><strong>Username:</strong> ${entry.username}</p>
                    <p><strong>Password:</strong> <span id="pwd-${entry.id}">••••••••</span></p>
                    <button onclick="revealPassword(${entry.id})">Reveal</button>
                    <button onclick="deletePassword(${entry.id})">Delete</button>
                `;
                section.appendChild(entryDiv);
            });

            passwordsContainer.appendChild(section);
        }
    }

    window.revealPassword = function (id) {
        revealId = id;
        systemPasswordModal.classList.remove("hidden");
        systemPasswordInput.value = "";
    };

    confirmPasswordBtn.addEventListener("click", async () => {
        const master_password = systemPasswordInput.value;
        const res = await fetch("/api/reveal", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: revealId, master_password }),
        });

        const result = await res.json();
        if (result.success) {
            document.getElementById("pwd-" + revealId).textContent = result.password;
            systemPasswordModal.classList.add("hidden");
        } else {
            alert(result.message || "Incorrect master password");
        }
    });

    window.deletePassword = async function (id) {
        const confirmDelete = confirm("Are you sure you want to delete this password?");
        if (!confirmDelete) return;

        await fetch("/api/delete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id }),
        });

        loadPasswords();
    };

    loadPasswords();
});
