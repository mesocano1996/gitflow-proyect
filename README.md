# GitFlow Proyecto Completo
# Puesta en producción segura – Trabajo final

Aplicación sencilla para simular un ciclo real de **SECDEVOPS** utilizando Python Flask, una API backend y contenedores Docker.

La aplicación gestiona usuarios de un colegio (alumnos y administrador), permite autenticarse y visualizar información básica obtenida desde una API protegida.

---

1. Objetivo de la práctica

Simular un ciclo de desarrollo seguro (SECDEVOPS) con:

- Frontend en **Flask**.
- Backend como **API REST** independiente.
- Autenticación y roles (admin / usuario normal).
- Contenedores Docker para front y back.
- Entorno virtual de Python.
- Pruebas automatizadas y Postman.
- Integración continua con GitHub Actions.



---

2. Estructura del proyecto

<<<<<<< HEAD
<<<<<<< HEAD
``` text
=======
```bash
>>>>>>> 6614d0d224968eddf9b102a819d1110df5e53acf
=======
```
>>>>>>> b465dd7a735cd5a6656b7e0430b3c543d98d22ac
gitflow-proyect/
├── app.py                   # Frontend Flask (web)
├── backend_api.py           # API backend
├── requirements.txt
├── Dockerfile.front
├── Dockerfile.api
├── docker-compose.yml
├── README.md
   
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── dashboard-admin.html
     |__admin.html 
└── tests/
    ├── test_auth.py
    └── test_api.py
    ├── test_dash_api.py
<<<<<<< HEAD
│ └── test_api_auth.py
 templates/ # HTML Bootstrap 5
    ├── base.html # Layout común + navbar
    ├── index.html # Home público
    ├── login.html # Formulario login
    ├── register.html # Formulario registro
    ├── dashboard.html # Alumno (notas+asistencia API)
    └── dashboard-admin.html # Admin (mismo + extras)
```
 
=======
    └── test_api_auth.py
>>>>>>> a3514c674cc94aecb22547141df74ac83d69c832

<<<<<<< HEAD
=======
````
>>>>>>> b465dd7a735cd5a6656b7e0430b3c543d98d22ac


<<<<<<< HEAD
=======


>>>>>>> 6614d0d224968eddf9b102a819d1110df5e53acf
3. Entornos virtuales / contenedores de desarrollo 

El desarrollo se ha aislado usando un entorno virtual de Python (venv) para no mezclar dependencias con otros proyectos.

Pasos usados:
```
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
python app.py
python backend_api.py
docker compose up --build
```
4. Autenticación del usuario y autorización 

La aplicación implementa:

Registro y login de usuarios mediante formularios Flask.

Persistencia de usuarios en una base de datos SQLite usando flask_sqlalchemy.

Contraseñas almacenadas hasheadas con generate_password_hash y validadas con check_password_hash.

Dos tipos de usuario:

- admin (creado automáticamente al iniciar la aplicación).

- alumno (usuarios registrados desde la web).

Flujo principal:

Al autenticarse, se guarda en session un diccionario con email, nombre_alumno, curso y rol.

Las vistas indican qué usuario se ha identificado.

Si el usuario tiene rol admin, el dashboard utiliza una plantilla distinta (dashboard-admin.html) y un estilo diferenciado (color de fondo / tarjeta distinta), además acceso a la lista de alumnos de su curso (admin.html).

El acceso a /dashboard comprueba siempre que haya sesión; si no la hay, redirige a /login.

5. Arquitectura front–back y API segura

La aplicación se divide en dos componentes:

5.1 Frontend (app.py)
Rutas principales:
```
/ – página de inicio.

/register – registro de alumnos.

/login – inicio de sesión.

/dashboard – panel de usuario / administrador.

/logout – cierre de sesión.

Plantillas Jinja2 (templates/*.html) para el contenido HTML.
```
Obtiene las notas y la asistencia del usuario llamando a la API backend.

5.2 Backend API (backend_api.py)
Endpoints de ejemplo:
```
GET /api/notas/<email>

GET /api/asistencia/<email>
```
Devuelven datos en formato JSON (datos de demostración definidos en memoria).

Todos los endpoints /api/... están protegidos por un token estático:

- El frontend envía el encabezado X-API-TOKEN.

- Si el token no coincide, la API devuelve 401 Unauthorized.

Con esto se cumple el requisito de tener un front Flask que se comunique con un back a través de una API utilizando un mecanismo seguro.

6. Aplicaciones en contenedores
   
Se han creado dos imágenes Docker:
```
Dockerfile.front → imagen para el frontend Flask.

Dockerfile.api → imagen para el backend API.
```
El fichero docker-compose.yml orquesta ambos servicios:
<<<<<<< HEAD
```

=======

```
>>>>>>> b465dd7a735cd5a6656b7e0430b3c543d98d22ac
docker-compose up --build
```
Configuración típica:

Frontend Flask: http://127.0.0.1:8000 (puerto host 8000 → contenedor 5000).

Backend API: http://127.0.0.1:5001 (puerto host 5001 → contenedor 5001).

Dentro de la red de Docker, el frontend se comunica con el backend usando el nombre de servicio backend en el puerto 5001.

7. OWASP Top 10 (web y APIs).

En owasp-seguridad.md se documenta cómo se han tenido en cuenta varios puntos de OWASP Top 10 para aplicaciones web y APIs. Resumen:

7.1 Aplicación web
A01 – Broken Access Control
Se valida la existencia de sesión en /dashboard y se diferencia el rol admin del rol alumno para mostrar vistas distintas.
```
# En /dashboard
if 'user' not in session:
    return redirect(url_for('login'))

# En /admin y /admin/notas/<alumno_email>
if 'user' not in session or session['user']['rol'] != 'admin':
    flash("❌ Acceso denegado. Solo admins.", "error")
    return redirect(url_for('dashboard'))
```
A02 – Cryptographic Failures
Las contraseñas se almacenan en la base de datos utilizando generate_password_hash, evitando guardar texto plano.
```
# En registro y creación admin
password_hash=generate_password_hash(password)

# En modelo Usuario
def comprobar_password(self, password):
    return check_password_hash(self.password_hash, password)

```
A03 – Injection
El acceso a la base de datos se realiza mediante SQLAlchemy, sin construir consultas SQL concatenando cadenas.
```
# ORM SQLAlchemy evita concatenación SQL
user = Usuario.query.filter_by(email=email).first()
db.session.add(nuevo)
db.session.commit()

```
A05 – Security Misconfiguration
El modo debug solo se usa en desarrollo. No se muestran trazas internas al usuario final.
```
# Debug solo desarrollo (desactivar en prod)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

```
7.2 API
Autenticación de la API
Todos los endpoints /api/... exigen el encabezado X-API-TOKEN. Si falta o es incorrecto, la API devuelve 401 Unauthorized.
```
# backend_api.py
API_TOKEN = "super-api-token-123"

def check_token():
    token = request.headers.get("X-API-TOKEN")
    return token == API_TOKEN

@app.before_request
def require_token():
    if request.path.startswith("/api/"):
        if not check_token():
            return jsonify({"error": "Unauthorized"}), 401
```
Gestión de errores
La API devuelve respuestas JSON simples ({"error": "Unauthorized"}) sin detalles internos de excepciones ni stacktraces.
```
# Respuesta simple sin stacktraces
return jsonify({"error": "Unauthorized"}), 401
```
## 8. Las pruebas se han implementado con pytest y se ejecutan con:

pytest

Contenido principal:
```
tests/test_auth.py
```
Pruebas del flujo de autenticación en app.py mediante test_client():
```
Login correcto con credenciales válidas.

Login incorrecto con contraseña errónea.
```
tests/test_api.py

Pruebas de la API backend (backend_api.py):

Acceso autorizado a /api/notas/<email> con token correcto.

Acceso no autorizado sin encabezado X-API-TOKEN.
```
```
## Tests Automatizados

### Pruebas Unitarias (2)
- `test_login_correcto.py` → Login válido → Dashboard 200 OK
- `test_login_incorrecto.py` → Login inválido → Alert danger

### Pruebas Integración (2)  
- `test_dash_api.py` → Dashboard + API notas/asistencia
- `test_api_auth.py` → API protegida (404 frontend / 401 backend)

### Ejecutar

pip install pytest
python -m pytest test/ -v
```
```
##  Pruebas API con Postman

### Endpoints protegidos

La API backend requiere header `X-API-TOKEN` para autorizar peticiones:

| Endpoint | Método | Autenticación | Respuesta |
|----------|--------|---------------|-----------|
| `/api/notas/alumno@colegio.es` | GET | Token requerido | `200 OK` JSON |
| `/api/asistencia/alumno@colegio.es` | GET | Token requerido | `200 OK` JSON |
| `/api/notas/*` (sin token) | GET |  Sin token | `401 Unauthorized` |

### Colección Postman

**Archivo:** `postman-gitflow.json` (incluido en repo)

**Importar:**
1. Postman → **Import** → **File**
2. Seleccionar `postman-gitflow.json`
3. Configurar variable `{{api_token}}` con token real
```
### Tests automatizados
```
pytest tests/ -v --tb=no
```

 9. Gestión de versiones, GitHub y automatización

El proyecto se ha versionado con git:

Rama principal main.

Ramas de características (Jorge1, Jorge2, etc.) que se han fusionado después en main siguiendo un flujo similar a git-flow.

El código se ha subido a GitHub en un repositorio público para poder reproducir el proyecto en otro entorno.

Se ha configurado un workflow de GitHub Actions (.github/workflows/tests.yml) que:

Instala Python y las dependencias indicadas en requirements.txt.

Ejecuta automáticamente pytest en cada push o pull_request.

Con esto se completa un ciclo de SECDEVOPS a pequeña escala: desarrollo aislado, seguridad básica (OWASP), pruebas automatizadas y despliegue en contenedores.
## CI/CD Automatizado
```
**GitHub Actions** → Tests + Docker en cada push/PR
```
[![CI Tests](https://github.com/mesocano1996/gitflow-proyect/actions/workflows/ci.yml/badge.svg)](https://github.com/mesocano1996/gitflow-proyect/actions)

Tests automáticos:
- 4 pytest → Login + API + Dashboard
- Docker build

<<<<<<< HEAD
<<<<<<< HEAD

<<<<<<< HEAD




=======
>>>>>>> 6614d0d224968eddf9b102a819d1110df5e53acf
=======
>>>>>>> b465dd7a735cd5a6656b7e0430b3c543d98d22ac
=======



>>>>>>> a3514c674cc94aecb22547141df74ac83d69c832
