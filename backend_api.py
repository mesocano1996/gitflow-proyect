from flask import Flask, jsonify, request

app = Flask(__name__)

API_TOKEN = "super-api-token-123"

# Asignaturas CEU Primaria (para CUALQUIER usuario)
ASIGNATURAS_PRIMARIA = [
    {"asignatura": "Lengua Castellana", "nota": "SC"},
    {"asignatura": "Matemáticas", "nota": "SC"},
    {"asignatura": "Ciencias de la Naturaleza", "nota": "SC"},
    {"asignatura": "Ciencias Sociales", "nota": "SC"},
    {"asignatura": "Inglés", "nota": "SC"},
    {"asignatura": "Educación Física", "nota": "SC"},
    {"asignatura": "Religión / Valores", "nota": "SC"},
    {"asignatura": "Educación Artística", "nota": "SC"},
]

# Asistencia por defecto
ASISTENCIA_DEFAULT = [
    {"fecha": "2026-03-01", "estado": "Presente"},
    {"fecha": "2026-03-02", "estado": "Presente"},
    {"fecha": "2026-03-03", "estado": "Ausente"},
]

# Datos demo
notas_demo = {"alumno@colegio.es": ASIGNATURAS_PRIMARIA}
asistencia_demo = {"alumno@colegio.es": ASISTENCIA_DEFAULT}

def get_notas_usuario(email):
    if email in notas_demo:
        return notas_demo[email]
    return ASIGNATURAS_PRIMARIA

def get_asistencia_usuario(email):
    if email in asistencia_demo:
        return asistencia_demo[email]
    return ASISTENCIA_DEFAULT

def check_token():
    token = request.headers.get("X-API-TOKEN")
    if token != API_TOKEN:
        return False
    return True

@app.before_request
def require_token():
    if request.path.startswith("/api/"):
        if not check_token():
            return jsonify({"error": "Unauthorized"}), 401

@app.route("/api/notas/<email>", methods=["POST"])
def update_notas(email):
    if request.headers.get("X-API-TOKEN") != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    
    global notas_demo
    notas_demo[email] = request.json
    return jsonify({"status": "updated", "notas": notas_demo[email]})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

@app.route("/api/asistencia/<email>")
def api_asistencia(email):
    return jsonify(get_asistencia_usuario(email))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

