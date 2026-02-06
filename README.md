# Flask Web Application Project

## 📌 Project Description

This is a secure Flask-based web application that implements **user authentication with email verification**. The application allows users to register, verify their email address via a secure token-based link, log in, and access a protected dashboard. Security best practices such as password hashing, session handling, rate limiting, and input validation are applied.

The project is suitable for learning or demonstrating **secure authentication workflows** in Flask and can be extended into larger applications.

---

## 🛠️ Technologies Used

* **Python** – Core programming language
* **Flask** – Web framework
* **Flask-Login** – User session management
* **Flask-SQLAlchemy** – ORM for database handling
* **SQLite** – Lightweight database
* **Flask-Mail** – Sending email verification links
* **itsdangerous** – Secure token generation
* **HTML5 / CSS3 / JavaScript** – Frontend
* **Git & GitHub** – Version control

---

## ⚙️ Installation Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Salmanul-faris-tech/Flask_Web_Application_Project.git
cd Flask_Web_Application_Project
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

Activate it:

* **Windows**

```bash
venv\Scripts\activate
```

* **Linux / macOS**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_app_password
```

> ⚠️ Do not push `.env` to GitHub. It is already ignored using `.gitignore`.

### 5️⃣ Run the application

```bash
python app.py
```

The app will be available at:

```
http://127.0.0.1:5000/
```

---

## ▶️ Usage Instructions

1. Open the application in your browser
2. Register a new account
3. Check your email and click the verification link
4. Log in after verification
5. Access the protected dashboard
6. Log out securely

Rate limiting protects the login page from brute-force attempts.

---

## 🖼️ Screenshots / Live Demo

### Screenshots

```
<img width="1920" height="873" alt="Home _ Welcome - Google Chrome 06-02-2026 15_32_59" src="https://github.com/user-attachments/assets/a3fb14a7-1572-4d8a-be17-f8050269d8c6" />

<img width="1920" height="877" alt="Home _ Welcome - Google Chrome 06-02-2026 15_33_57" src="https://github.com/user-attachments/assets/198677ab-5836-4b5f-b672-d6316edd3ce4" />

<img width="1920" height="875" alt="Home _ Welcome - Google Chrome 06-02-2026 15_34_36" src="https://github.com/user-attachments/assets/0aed0015-53c7-4885-b4c7-0a2c11162d6c" />

<img width="1920" height="865" alt="Home _ Welcome - Google Chrome 06-02-2026 15_42_01" src="https://github.com/user-attachments/assets/36c4b875-eb3a-4ac3-86a4-43ff768d6406" />

```

### Live Demo

🚧 Live demo not deployed yet.

---

## 🔐 Security Features

* Strong password policy
* Email verification before login
* Password hashing
* Session handling with Flask-Login
* Rate limiting for login attempts
* Input validation and sanitization

---

## 📄 License

This project is for educational and demonstration purposes.

---

## 👤 Author

**Salmanul Faris**
GitHub: [https://github.com/Salmanul-faris-tech](https://github.com/Salmanul-faris-tech)

---

⭐ If you find this project useful, feel free to star the repository!
