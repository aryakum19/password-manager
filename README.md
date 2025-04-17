# 🔐 Password Manager

A secure, stylish, and full-featured password manager built using **Flask**, **SQLite**, **bcrypt**, and **Fernet encryption**, with a modern **glassmorphism web frontend**.

## ✨ Features

- 🔑 User Signup & Login (with bcrypt-hashed master password)
- 🔐 AES-encrypted password storage using Fernet
- 📋 Add, view (grouped by service), and delete saved passwords
- 👁️ Reveal passwords securely with master password verification
- ⚙️ Password strength checker
- 🎲 Random password generator
- 🧼 Clean UI with glassmorphism and responsive layout
- 📤 Export-ready structure with separation of backend and frontend

---

## 📁 Project Structure

<pre>
password-manager/
├── backend/
│   ├── app.py                # Main Flask app
│   ├── passwords.db          # SQLite DB (auto-created)
│   ├── secret.key            # Encryption key (auto-created)
├── frontend/
│   ├── static/
│   │   ├── styles.css        # CSS (modern glass look)
│   │   └── script.js         # All frontend logic
│   ├── templates/
│   │   ├── dashboard.html    # User dashboard
│   │   ├── login.html        # Login page
│   │   └── signup.html       # Signup page
├── README.md                 # Project documentation
</pre>

---

## 🚀 Getting Started

### 1. Clone the Repository

<pre>bash
git clone https://github.com/yourusername/password-manager.git
cd password-manager
</pre>

### 2. Create a Virtual Environment (Recommended)

<pre>bash
python -m venv venv
source venv/bin/activate  # On Windows use \`venv\Scripts\activate\`
</pre>

### 3. Install Dependencies

<pre>bash
pip install -r requirements.txt
</pre>

If **requirements.txt** is not available, manually install:

<pre>bash
pip install flask flask-bcrypt cryptography
</pre>

---

### 4. Run the App

\`\`\`bash
cd backend
python app.py
\`\`\`

The app will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔒 Encryption Details

- Passwords are encrypted using **Fernet (AES in CBC mode with HMAC)**.
- A \`secret.key\` is generated once and used for symmetric encryption/decryption.
- Master passwords are hashed using **bcrypt** for secure storage.

---

## 📦 Features in Detail

### ➕ Add Password
- Add credentials (service, username, password).
- Passwords are encrypted before saving.

### 📁 View Passwords
- Passwords grouped by service.
- Click reveal requires master password confirmation.

### ❌ Delete Password
- Delete individual entries.
- Confirmation popup for all deletions.

### 💪 Password Strength
- Passwords are rated based on length, complexity, and entropy.

### 🔁 Password Generator
- Click the generate button to fill a secure, random password.

---

## 🖥️ Frontend Technologies

- **HTML5** + **CSS3** (Glassmorphism)
- **Vanilla JavaScript**
- Responsive layout

---

## 🧪 Backend Technologies

- **Flask** for the web server
- **SQLite** for local data storage
- **bcrypt** for hashing
- **cryptography.fernet** for encryption

---

## 🤝 Contributions

Feel free to fork and contribute! Open issues or submit pull requests for suggestions and fixes.
