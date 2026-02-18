from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super-secret-key-gitflow-2026"

# Configuración base de datos PostgreSQL
DB_CONFIG = {
    "host": "host.docker.internal",
    "port": 5432,
    "database": "miapp",
    "user": "usuario",
    "password": "password123"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre_colegio = request.form["nombre_colegio"]
        nombre_alumno = request.form["nombre_alumno"]
        email = request.form["email"]
        curso = request.form["curso"]
        password = request.form["password"]
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar si email ya existe
        cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cur.fetchone():
            flash("❌ El email ya está registrado", "error")
            cur.close()
            conn.close()
            return render_template("register.html")
        
        # Insertar nuevo usuario (password plano por simplicidad)
        cur.execute("""
            INSERT INTO usuarios (nombre_colegio, nombre_alumno, email, curso, password) 
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre_colegio, nombre_alumno, email, curso, password))
        
        conn.commit()
        cur.close()
        conn.close()
        flash("✅ ¡Usuario registrado correctamente!", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        # Verificar credenciales (password plano)
        if user and user[5] == password:  # password en posición 5
            session["user"] = {
                "id": user[0],
                "nombre_colegio": user[1],
                "nombre_alumno": user[2],
                "email": user[3],
                "curso": user[4]
            }
            flash("🎉 ¡Bienvenido " + user[2] + "!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Email o contraseña incorrectos", "error")
    
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("⚠️ Debes iniciar sesión", "error")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM materiales_primaria ORDER BY curso, asignatura")
    materiales = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("dashboard.html", materiales=materiales, user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    flash("👋 Sesión cerrada correctamente", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
