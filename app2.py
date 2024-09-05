from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')

JSON_DB_PATH = 'instance/database.json'

# Función para cargar datos desde el archivo JSON
def load_data():
    if not os.path.exists(JSON_DB_PATH):
        return []
    with open(JSON_DB_PATH, 'r') as file:
        return json.load(file)

# Función para guardar datos en el archivo JSON
def save_data(data):
    with open(JSON_DB_PATH, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def visitor_page():
    return render_template('visitor.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        agreement = request.form.get('agreement') == 'on'

        # Cargar los datos existentes
        users = load_data()

        # Crear un nuevo usuario
        new_user = {
            'id': len(users) + 1,
            'nombre': nombre,
            'apellido': apellido,
            'agreement': agreement,
            'fecha_creacion': datetime.utcnow().isoformat()
        }

        # Añadir el nuevo usuario y guardar los datos
        users.append(new_user)
        save_data(users)

        return jsonify({"message": "Datos recibidos correctamente"}), 200
    except Exception as e:
        app.logger.error(f"Error al subir datos: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/admin/users', methods=['GET'])
def get_users():
    users = load_data()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
