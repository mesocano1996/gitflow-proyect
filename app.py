from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import requests
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super-secret-key-gitflow-2026"

# BD SQLite local
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

API_URL = "http://backend:5001"  # en local puro cambia a "http://127.0.0.1:5001"
API_TOKEN = "super-api-token-123"


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre_colegio = db.Column(db.String(120), nullable=False)
    nombre_alumno = db.Column(db.String(120), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="alumno")
    password_hash = db.Column(db.String(255), nullable=False)

    def comprobar_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(email="admin@colegio.es").first():
        admin = Usuario(
            email="admin@colegio.es",
            nombre_colegio="Colegio Central",
            nombre_alumno="Admin Sistema",
            curso="N/A",
            rol="admin",
            password_hash=generate_password_hash("admin123"),
        )
        db.session.add(admin)
        db.session.commit()


def get_user():
    return session.get("user")


@app.route("/")
def index():
    return render_template("index.html", user=get_user())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if Usuario.query.filter_by(email=email).first():
            flash("❌ Ese email ya está registrado", "error")
            return redirect(url_for("register"))

        nuevo = Usuario(
            email=email,
            nombre_colegio=request.form["nombre_colegio"],
            nombre_alumno=request.form["nombre_alumno"],
            curso=request.form["curso"],
            rol="alumno",
            password_hash=generate_password_hash(password),
        )
        db.session.add(nuevo)
        db.session.commit()

        flash("✅ ¡Usuario registrado como alumno!", "success")
        return redirect(url_for("login"))

    return render_template("register.html", user=get_user())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        user = Usuario.query.filter_by(email=email).first()
        if user and user.comprobar_password(password):
            session["user"] = {
                "email": user.email,
                "nombre_colegio": user.nombre_colegio,
                "nombre_alumno": user.nombre_alumno,
                "curso": user.curso,
                "rol": user.rol,
            }
            flash(f"🎉 ¡Bienvenido {user.nombre_alumno}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Credenciales incorrectas", "error")

    return render_template("login.html", user=get_user())


@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_email = session['user']['email']
    
    # CONFIGURACIÓN FIJA
    API_URL = "http://127.0.0.1:5001"
    API_TOKEN = "super-api-token-123"
    
    try:
        headers = {"X-API-TOKEN": API_TOKEN}
        
        # NOTAS - funciona para CUALQUIER email
        notas_resp = requests.get(
            f"{API_URL}/api/notas/{user_email}", 
            headers=headers, 
            timeout=5
        )
        notas_resp.raise_for_status()
        notas = notas_resp.json()
        
        # ASISTENCIA - funciona para CUALQUIER email  
        asistencia_resp = requests.get(
            f"{API_URL}/api/asistencia/{user_email}", 
            headers=headers, 
            timeout=5
        )
        asistencia_resp.raise_for_status()
        asistencia = asistencia_resp.json()
        
    except Exception as e:
        print(f"ERROR API: {e}")  # Debug en consola
        flash("⚠️ No se ha podido conectar con la API de backend.", "error")
        notas = []
        asistencia = []
    
    return render_template("dashboard.html", user=session['user'], notas=notas, asistencia=asistencia)

@app.route("/logout")
def logout():
    session.clear()
    flash("👋 Sesión cerrada", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
