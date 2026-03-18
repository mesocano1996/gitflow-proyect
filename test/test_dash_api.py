import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

@patch('app.requests.get')  # ← MOCK requests.get de app.py
def test_dashboard_con_api(mock_get, client):
    # Simula respuestas API
    mock_get.side_effect = [
        MagicMock(status_code=200, json=lambda: [{"asignatura": "Lengua Castellana", "nota": "SC"}]),
        MagicMock(status_code=200, json=lambda: [{"fecha": "2026-03-01", "estado": "Presente"}])
    ]
    
    # Login admin (el que SÍ existe)
    client.post('/login', data={
        'email': 'admin@colegio.es',
        'password': 'admin123'
    })
    
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b"Lengua Castellana" in response.data
    assert b"Presente" in response.data
    print("✅ test_dash_api.py: Dashboard + API MOCK OK")
