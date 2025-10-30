from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import db, Alumno, Clase, Asistencia

import datetime

profesor_bp = Blueprint("profesor", __name__)

@profesor_bp.route("/dashboard")
def dashboard():
    alumnos = Alumno.query.all()
    clases = Clase.query.all()
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    asistencias = Asistencia.query.filter_by(fecha=hoy).all()
    alumnos_asistidos = {a.alumno_id for a in asistencias}

    return render_template(
        "dashboard.html",
        alumnos=alumnos,
        clases=clases,
        alumnos_asistidos=alumnos_asistidos
    )


@profesor_bp.route("/agregar-alumno", methods=["POST"])
def agregar_alumno():
    nombre = request.form.get("nombre")
    dni = request.form.get("dni")
    clase_id = request.form.get("clase_id")

    if not nombre or not dni or not clase_id:
        flash("⚠️ Faltan datos", "error")
    elif Alumno.query.filter_by(dni=dni).first():
        flash("⚠️ DNI ya registrado", "error")
    else:
        alumno = Alumno(nombre=nombre, dni=dni)
        db.session.add(alumno)
        clase = Clase.query.get(clase_id)
        clase.alumnos.append(alumno)
        db.session.commit()
        flash("✅ Alumno agregado con éxito", "exito")

    return redirect(url_for("profesor.dashboard"))
