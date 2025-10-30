from flask import Blueprint, request, jsonify, render_template, send_file
from models.database import db, Alumno, Clase, Asistencia, ShortCode
import datetime
import pandas as pd
from sqlalchemy import func
from extensions import socketio


attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/alumno", methods=["GET"])
def alumno_form():
    return render_template("alumno.html", mensaje=None)


@attendance_bp.route("/asistencia", methods=["GET", "POST"])
def marcar_asistencia():
    
    mensaje = None
    dni = request.form.get("dni")
    short_code = request.form.get("short_code")

    if not dni or not short_code:
        return render_template("alumno.html", mensaje="Faltan datos")

    # Buscar el código
    sc = ShortCode.query.filter_by(code=short_code).first()
    if not sc:
        return render_template("alumno.html", mensaje="❌ Código no válido")

    if sc.expires_at < datetime.datetime.utcnow():
        return render_template("alumno.html", mensaje="Código expirado")

    clase_id = sc.clase_id
    sc.used_count += 1
    clase = Clase.query.get(clase_id)
    db.session.commit()

    # Buscar alumno por DNI
    alumno = Alumno.query.filter_by(dni=dni).first()
    if not alumno:
        return render_template("alumno.html", mensaje="Alumno no registrado")

    if alumno not in clase.alumnos:
        return render_template("alumno.html", mensaje="Alumno no pertenece a esta clase")

    # Evitar doble registro
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    existe = Asistencia.query.filter_by(
        alumno_id=alumno.id, clase_id=clase_id, fecha=hoy
    ).first()
    if existe:
        return render_template("alumno.html", mensaje="Ya existe registro de asistencia")

    # Registrar asistencia
    ahora = datetime.datetime.now()
    registro = Asistencia(
        alumno_id=alumno.id,
        clase_id=clase_id,
        fecha=ahora.strftime("%Y-%m-%d"),
        hora=ahora.strftime("%H:%M:%S"),
    )
    db.session.add(registro)
    db.session.commit()

    socketio.emit('asistencia_actualizada', {"alumno_id": alumno.id, "estado": "asistido"})

    return render_template("alumno.html", mensaje="✅ Asistencia registrada con éxito")

