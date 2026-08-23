import os
import time

import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/login_db"
)


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    max_retries = 10

    for attempt in range(1, max_retries + 1):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)

            conn.commit()
            cursor.close()
            conn.close()

            print("Database connection successful.")
            return

        except psycopg2.OperationalError as error:
            print(
                f"Database belum siap. "
                f"Percobaan {attempt}/{max_retries}..."
            )

            if attempt == max_retries:
                print("Gagal terhubung ke database.")
                raise error

            time.sleep(2)


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            message = "Username dan password wajib diisi."
            return render_template("register.html", message=message)

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
                """,
                (username, hashed_password)
            )

            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for("login"))

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            cursor.close()
            conn.close()

            message = "Username sudah digunakan."

    return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT username, password
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["username"] = user[0]
            return redirect(url_for("dashboard"))

        message = "Username atau password salah."

    return render_template("login.html", message=message)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()

        return "Application and Database are connected!"

    except Exception as error:
        return f"Database connection failed: {error}", 500


if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=5000
    )