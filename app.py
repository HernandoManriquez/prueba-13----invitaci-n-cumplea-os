from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    agreement = db.Column(db.Boolean, nullable=False)
    video_filename = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

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
        video = request.files.get('user-video')

        video_filename = None
        if video and video.filename != '':
            filename = secure_filename(video.filename)
            video_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            video.save(upload_path)

        new_user = User(nombre=nombre, apellido=apellido, agreement=agreement, video_filename=video_filename)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Datos recibidos correctamente"}), 200
    except Exception as e:
        app.logger.error(f"Error al subir datos: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/admin/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [{
        'id': user.id,
        'nombre': user.nombre,
        'apellido': user.apellido,
        'agreement': user.agreement,
        'video_filename': user.video_filename,
        'fecha_creacion': user.fecha_creacion.isoformat()
    } for user in users]
    return jsonify(users_data)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def init_db():
    with app.app_context():
        db.create_all()
        app.logger.info("Base de datos inicializada.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)