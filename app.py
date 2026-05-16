from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DB_NAME = os.path.join(os.path.dirname(__file__), "tareas.db")

# 1. Configuración de Base de Datos SQLite
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Crear tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tarea (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL
            )
        ''')
        # Insertar datos de prueba iniciales si la base está vacía
        cursor.execute('SELECT COUNT(*) FROM tarea')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO tarea (descripcion) VALUES (?)', ("Aprobar evaluación sustitutoria",))
            cursor.execute('INSERT INTO tarea (descripcion) VALUES (?)', ("Configurar entorno Docker",))
            cursor.execute('INSERT INTO tarea (descripcion) VALUES (?)', ("Implementar pruebas con Pytest",))
        conn.commit()

# Inicializar la base de datos siempre que se importe el módulo
init_db()

@app.route('/_health')
def _health():
    return 'ok'

# 2. Ruta Frontend (Retorna la interfaz HTML)
@app.route('/')
def index():
    return render_template('index.html')

# 3. Rutas API REST (Endpoints)
@app.route('/api/tareas', methods=['GET'])
def obtener_tareas():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, descripcion FROM tarea')
        tareas = [{'id': row[0], 'descripcion': row[1]} for row in cursor.fetchall()]
    return jsonify(tareas), 200

@app.route('/api/tareas', methods=['POST'])
def crear_tarea():
    data = request.get_json()
    if not data or 'descripcion' not in data:
        return jsonify({'error': 'Falta el campo descripcion'}), 400
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tarea (descripcion) VALUES (?)', (data['descripcion'],))
        conn.commit()
        nueva_id = cursor.lastrowid
        
    return jsonify({'id': nueva_id, 'descripcion': data['descripcion']}), 201

if __name__ == '__main__':
    # Inicializa la base de datos antes de arrancar el servidor
    init_db()
    app.run(host='0.0.0.0', port=5000)