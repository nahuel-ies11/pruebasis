from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.database import db, Alumno, Clase, Asistencia, Profesor

import datetime

profesor_bp = Blueprint("profesor", __name__)

@profesor_bp.route("/dashboard")
def dashboard():
    alumnos = Alumno.query.all()
    clases = Clase.query.all()
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    asistencias = Asistencia.query.filter_by(fecha=hoy).all()
    alumnos_asistidos = {a.alumno_id for a in asistencias}
    profesor = Profesor.query.first()

    return render_template(
        "dashboard.html",
        alumnos=alumnos,
        clases=clases,
        alumnos_asistidos=alumnos_asistidos,
        profesor=profesor
    )


@profesor_bp.route("/agregar-alumno", methods=["POST"])
def agregar_alumno():
    data = request.get_json()
    print("JSON recibido:", request.get_json())

    nombre = data.get("nombre")
    dni = data.get("dni")
    clase_id = data.get("clase_id")

    if not nombre or not dni or not clase_id:
        return jsonify({"success": False, "message": "Faltan datos"}), 400

    clase = Clase.query.get(clase_id)
    if not clase:
        return jsonify({"success": False, "message": "Clase no encontrada"}), 404

    if Alumno.query.filter_by(dni=dni).first():
        return jsonify({"success": False, "message": "Alumno con este DNI ya existe"}), 400

    alumno = Alumno(nombre=nombre, dni=dni)
    db.session.add(alumno)
    clase.alumnos.append(alumno)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Alumno agregado con éxito",
        "alumno": {"id": alumno.id, "nombre": alumno.nombre, "dni": alumno.dni}
    })

