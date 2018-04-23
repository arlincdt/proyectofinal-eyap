from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.fechas.fecha import Fecha

fecha_blueprint = Blueprint('fechas', __name__)

@fecha_blueprint.route('/fecha', methods=['GET', 'POST'])
def fecha():
    fecha = Fecha.getFecha()
    if request.method == 'POST':
        fecha = request.form['fecha']
        Fecha.updateFecha(fecha)
    fecha = Fecha.getFecha()

    return render_template("fecha.jinja2", fecha=fecha)





