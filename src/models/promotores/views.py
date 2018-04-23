from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.promotores.promotor import Promotor
from src.models.fechas.fecha import Fecha

promotor_blueprint = Blueprint('promotores', __name__)

@promotor_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    fecha = Fecha.getFecha()
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        try:
            if Promotor.loginValid(nombre, password):
                session['nombre']=nombre
                return redirect(url_for("clientes.getClientes", fecha=fecha))
            else:
                return "Invalid login"
        except:
            return "Invalid login"

    return render_template("login.jinja2", fecha = fecha)


@promotor_blueprint.route('/logout')
def logout():
    session['nombre'] = None
    session['cId'] = None
    return redirect(url_for('home'))




