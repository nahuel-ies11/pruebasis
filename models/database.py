from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ─────────── MODELOS ───────────

class Profesor(db.Model):
    __tablename__ = "profesor"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)


# Relación many-to-many Alumno <-> Clase
alumno_clase = db.Table(
    "alumno_clase",
    db.Column("alumno_id", db.Integer, db.ForeignKey("alumno.id"), primary_key=True),
    db.Column("clase_id", db.Integer, db.ForeignKey("clase.id"), primary_key=True)
)


class Alumno(db.Model):
    __tablename__ = "alumno"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)  # identificador único

    # Relación con Clase
    clases = db.relationship("Clase", secondary=alumno_clase, back_populates="alumnos")


class Clase(db.Model):
    __tablename__ = "clase"
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(120), nullable=False)

    profesor_id = db.Column(db.Integer, db.ForeignKey("profesor.id"), nullable=False)
    profesor = db.relationship("Profesor", backref="clases")

    alumnos = db.relationship("Alumno", secondary=alumno_clase, back_populates="clases")


class Asistencia(db.Model):
    __tablename__ = "asistencia"
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey("alumno.id"), nullable=False)
    clase_id = db.Column(db.Integer, db.ForeignKey("clase.id"), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    hora = db.Column(db.String(20), nullable=False)

    alumno = db.relationship("Alumno", backref="asistencias")
    clase = db.relationship("Clase", backref="asistencias")


class ShortCode(db.Model):
    __tablename__ = "shortcode"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, index=True, nullable=False)
    clase_id = db.Column(db.Integer, db.ForeignKey("clase.id"), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    clase = db.relationship("Clase", backref="shortcodes")
