from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

app.config["MAIL_USERNAME"] = "your_mail@gmail.com"
app.config["MAIL_PASSWORD"] = "you_app_password"
app.config["MAIL_DEFAULT_SENDER"] = "your_mail@gmail.com"

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            if not user.is_verified:
                return render_template("index.html", error="Please verify your email first.")
            login_user(user)
            return redirect(url_for("dashboard"))

        return render_template("index.html", error="Invalid username or password")

    return render_template("index.html")

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def username_sec_check(username):
    return re.fullmatch(r"[A-Za-z0-9_]+", username)

@app.route("/resend-verification", methods=["POST"])
@limiter.limit("3 per hour")
def resend_verification():
    email = request.form.get("email")
    user = Users.query.filter_by(email=email).first()

    if not user:
        return render_template("index.html", error="Account not found.")

    if user.is_verified:
        return render_template("index.html", error="Email already verified.")

    token = serializer.dumps(email, salt="email-verify")
    verify_url = url_for("verify_email", token=token, _external=True)

    msg = Message(
        subject="Verify your email",
        recipients=[email],
        body=f"Click the link to verify your account:\n{verify_url}"
    )
    mail.send(msg)

    return "Verification email resent. Please check your inbox."

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        #Password strength check
        if not is_strong_password(password):
            return render_template(
                "register.html",
                error="Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
            )

        #Username validation
        if not username_sec_check(username):
            return render_template(
                "register.html",
                error="Don't use special characters in username like <>$#"
            )

        #CHECK IF EMAIL ALREADY EXISTS (THIS IS THE PART YOU ASKED ABOUT)
        existing_user = Users.query.filter_by(email=email).first()

        if existing_user:
            if not existing_user.is_verified:
                # Resend verification email
                token = serializer.dumps(email, salt="email-verify")
                verify_url = url_for("verify_email", token=token, _external=True)

                msg = Message(
                    subject="Verify your email",
                    recipients=[email],
                    body=f"Click the link to verify your account:\n{verify_url}"
                )
                mail.send(msg)

                return "Account exists but not verified. Verification email resent."

            return render_template("register.html", error="Email already registered!")

        # 4️⃣ Username already taken
        if Users.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already taken!")

        # 5️⃣ Create new unverified user
        hashed_password = generate_password_hash(password)

        new_user = Users(
            username=username,
            email=email,
            password=hashed_password,
            is_verified=False
        )
        db.session.add(new_user)
        db.session.commit()

        # 6️⃣ Send verification email
        token = serializer.dumps(email, salt="email-verify")
        verify_url = url_for("verify_email", token=token, _external=True)

        msg = Message(
            subject="Verify your email",
            recipients=[email],
            body=f"Click the link to verify your account:\n{verify_url}"
        )
        mail.send(msg)

        return "Verification email sent! Please check your inbox."

    return render_template("register.html")


@app.route("/verify/<token>")
def verify_email(token):
    try:
        email = serializer.loads(
            token,
            salt="email-verify",
            max_age=3600  # 1 hour
        )
    except:
        return "Verification link expired or invalid."

    user = Users.query.filter_by(email=email).first()

    if user.is_verified:
        return "Email already verified."

    user.is_verified = True
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(debug=True)
