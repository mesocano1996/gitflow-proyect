from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def materiales():
    conn = psycopg2.connect(
        host="host.docker.internal",
        port=5432,
        database="miapp",
        user="usuario",
        password="password123"
    )
    cur = conn.cursor()
    cur.execute("SELECT asignatura, material, cantidad, curso FROM materiales_primaria ORDER BY curso")
    materiales = cur.fetchall()
    cur.close()
    conn.close()
    
    html = "<h1>📚 Material Primaria España</h1><table border='1'>"
    html += "<tr><th>Asignatura</th><th>Material</th><th>Cant.</th><th>Curso</th></tr>"
    for mat in materiales:
        html += f"<tr><td>{mat[0]}</td><td>{mat[1]}</td><td>{mat[2]}</td><td>{mat[3]}</td></tr>"
    html += "</table>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
