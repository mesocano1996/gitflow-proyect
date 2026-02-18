from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "super-secret-key-gitflow-2026"

# Datos demo (sin base de datos)
usuarios_demo = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        usuarios_demo[email] = {
            "nombre_colegio": request.form["nombre_colegio"],
            "nombre_alumno": request.form["nombre_alumno"],
            "curso": request.form["curso"]
        }
        flash("✅ ¡Usuario registrado!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        if email in usuarios_demo:
            session["user"] = usuarios_demo[email]
            flash(f"🎉 ¡Bienvenido {usuarios_demo[email]['nombre_alumno']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Email o contraseña incorrectos", "error")
    
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    flash("👋 Sesión cerrada", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
