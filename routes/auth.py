from flask import Blueprint, request, jsonify
from models.database import db, Clase, ShortCode
from datetime import datetime, timedelta
import random
import string

auth_bp = Blueprint("auth", __name__)

def crear_short_code_para_clase(clase_id, minutos_validez=5):
    """Genera un shortcode de 6 dígitos para una clase y lo guarda en la BD."""
    codigo = "".join(random.choices(string.digits, k=6))  # ejemplo: 483920
    expires_at = datetime.utcnow() + timedelta(minutes=minutos_validez)

    sc = ShortCode(code=codigo, clase_id=clase_id, expires_at=expires_at)  # 👈 code
    db.session.add(sc)
    db.session.commit()
    return sc

# 🔹 Ruta para generar shortcode
@auth_bp.route("/generar-shortcode", methods=["POST"])
def generar_shortcode():
    data = request.get_json()

    clase_id = data.get("clase_id")
    minutos = data.get("minutos", 5)

    if not clase_id:
        return jsonify({"error": "clase_id es requerido"}), 400

    # Validar que la clase exista
    clase = Clase.query.get(clase_id)
    if not clase:
        return jsonify({"error": "Clase no encontrada"}), 404

    # Generar el shortcode
    sc = crear_short_code_para_clase(clase_id, minutos_validez=int(minutos))

    return jsonify({
        "shortcode": sc.code, 
        "clase_id": sc.clase_id,
        "expires_at": sc.expires_at.isoformat()
    })
