import pytest
import sqlite3
import os
from app import app, init_db
import app as mi_app

# Usar una base de datos exclusiva para pruebas
TEST_DB = "test_tareas.db"

@pytest.fixture
def cliente():
    # Apuntar la aplicación a la DB de pruebas
    mi_app.DB_NAME = TEST_DB
    
    # Limpiar cualquier rastro anterior y crear la estructura nueva
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    mi_app.init_db()
    
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        yield cliente
        
    # Limpiar el archivo de pruebas al terminar
    if os.path.exists(TEST_DB):
        try:
            sqlite3.connect(TEST_DB).close()
            os.remove(TEST_DB)
        except PermissionError:
            pass


def test_crear_y_obtener_tarea(cliente):
    # Probar endpoint POST (Creación)
    respuesta_post = cliente.post('/api/tareas', json={'descripcion': 'Prueba de validación'})
    assert respuesta_post.status_code == 201
    
    # Probar endpoint GET (Consulta) y verificar que se insertó en SQLite
    respuesta_get = cliente.get('/api/tareas')
    data = respuesta_get.get_json()
    
    # Debería haber 4 tareas: las 3 predeterminadas + 1 que acabamos de crear en la prueba
    assert len(data) == 4
    # Validar que la última tarea sea la que inyectamos
    assert data[-1]['descripcion'] == 'Prueba de validación'
