from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.clientes.cliente import Cliente
from src.models.promotores.promotor import Promotor
from src.models.fechas.fecha import Fecha
from src.models.inversiones.inversion import Inversion
from src.models.fondo import Fondo

cliente_blueprint = Blueprint('clientes', __name__)

@cliente_blueprint.route('/muesta_clientes')
def getClientes():
    fecha = Fecha.getFecha()
    promotor = Promotor.getByNombre(session['nombre'])
    ganancias = Fondo.getFondo().ganancias
    if promotor.isAdmin:
        clientes = Cliente.getAllClientes()
    else:
        clientes = Cliente.getClientesByPromotor(promotor.nombre)
    
    valoresActuales = []
    if clientes:
        for cliente in clientes:
            suma = 0
            invs = Inversion.getByCId(cliente.cId)
            if invs:
                for inv in invs:
                    monto = inv.getMontoActual()
                    suma = suma + monto
            valoresActuales.append(suma)

    return render_template('clientes.jinja2', fecha=fecha, promotor=promotor, clientes=clientes, valoresActuales = valoresActuales, ganancias = ganancias)

@cliente_blueprint.route('/nuevoCliente', methods=['GET', 'POST'])
def nuevoCliente():
    
    if request.method == 'POST':
        promotor = Promotor.getByNombre(session['nombre'])
        nombre = request.form['nombre']
        saldoInicial = request.form['saldoInicial']
        cliente = Cliente(1, nombre, saldoInicial, 0, promotor.nombre)
        cliente.saveToDb()

        return redirect(url_for('clientes.getClientes'))

    fecha = Fecha.getFecha()
    return render_template("nuevo_cliente.jinja2", fecha=fecha)

