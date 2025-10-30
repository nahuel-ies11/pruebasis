from flask import Flask
from config import DATABASE_URI
from models.database import db, Profesor, Clase
from routes.auth import auth_bp
from routes.attendance import attendance_bp
from routes.profesor import profesor_bp
from extensions import socketio 


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Registrar rutas
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(attendance_bp, url_prefix="/")
app.register_blueprint(profesor_bp, url_prefix="/profesor")

app.config["SECRET_KEY"] = "una_clave_muy_segura_y_larga_aqui"

socketio.init_app(app) 

# Inicializar DB con datos de ejemplo
with app.app_context():
    db.create_all()
    if not Profesor.query.first():
        profesor = Profesor(nombre="Profesor Demo")
        db.session.add(profesor)
        db.session.commit()
        clase = Clase(materia="Informatica", profesor_id=profesor.id)
        db.session.add(clase)
        db.session.commit()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)

