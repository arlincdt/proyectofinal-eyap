from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.clientes.cliente import Cliente
from src.models.promotores.promotor import Promotor
from src.models.fechas.fecha import Fecha
from src.models.inversiones.inversion import Inversion
from src.models.tasa import Tasa
from src.models.fondo import Fondo
from datetime import timedelta
import time

inversion_blueprint = Blueprint('inversiones', __name__)

@inversion_blueprint.route('/<string:cId>', methods=['GET', 'POST'])
def getInversionesCliente(cId):
    cliente = Cliente.getByCId(cId)
    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        cliente.updateSaldoVista(cantidad)


    fecha = Fecha.getFecha()
    promotor = Promotor.getByNombre(session['nombre'])
    
    inversiones = Inversion.getByCId(cId)
    session['cId'] = cId

    tasas = []
    montosActuales = []
    if inversiones:
        for inversion in inversiones:
            tasa = Tasa.getByTId(inversion.tId)
            tasas.append(tasa)
            montoActual = inversion.getMontoActual()
            montosActuales.append(montoActual)
    
    sumMontosActuales = int(sum(montosActuales))

    return render_template('inversiones.jinja2', fecha=fecha, promotor=promotor, cliente = cliente, inversiones = inversiones, tasas = tasas, montosActuales = montosActuales, sumMontosActuales = sumMontosActuales)


@inversion_blueprint.route('/', methods=['GET', 'POST'])
def nuevaInversion():
    
    if request.method == 'POST':
        fecha = Fecha.getFecha()
        tId = request.form['tId']
        tasa = Tasa.getByTId(tId)
        cId = session['cId']
        cliente = Cliente.getByCId(cId)
        fechaInicial = fecha.fechaActual
        fechaFinal = fechaInicial + timedelta(days=tasa.periodoEnMeses*30)
        
        montoInicial = request.form['montoInicial']
        if cliente.saldoVista < int(montoInicial):
            return "No tiene fondos"
        montoFinal = float(montoInicial) * (float(tasa.interesTotal)/float(100)+1)

        inversion = Inversion(0, cId, fechaInicial, fechaFinal, tId, montoInicial, montoFinal)
        inversion.saveToDb()

        
        cliente.updateSaldoVista(-1*int(montoInicial))
        session['cId'] = None

        return redirect(url_for('inversiones.getInversionesCliente', cId = cId ))

    fecha = Fecha.getFecha()
    return render_template("nueva_inversion.jinja2", fecha=fecha)


@inversion_blueprint.route('reinvertirMismaCantidad/<string:iId>')
def reinvertirMismaCantidad(iId):
    iId = int(iId)
    fechaActual = Fecha.getFecha().fechaActual
    inversionVieja = Inversion.getByIId(iId)
    tasa = Tasa.getByTId(inversionVieja.tId)
    cliente = Cliente.getByCId(inversionVieja.cId)
    ganancias = inversionVieja.montoFinal - inversionVieja.montoInicial
    gananciasCliente = ganancias * 0.9
    gananciasFondo = ganancias * 0.1
    cliente.updateSaldoVista(gananciasCliente)
    gananciasActualesFondo = int(Fondo.getFondo().ganancias)
    Fondo.getFondo().updateGanancias(gananciasActualesFondo + gananciasFondo)

    montoInicial = inversionVieja.montoInicial
    montoFinal = float(montoInicial) * (float(tasa.interesTotal)/float(100)+1)
    inversionNueva = Inversion(0, cliente.cId, fechaActual, fechaActual + timedelta(days=tasa.periodoEnMeses*30), tasa.tId, montoInicial, montoFinal )
    inversionNueva.saveToDb()

    inversionVieja.deleteFromDb()

    return redirect(url_for('inversiones.getInversionesCliente', cId = cliente.cId))

@inversion_blueprint.route('reinvertirTodo/<string:iId>')
def reinvertirTodo(iId):
    iId = int(iId)
    fechaActual = Fecha.getFecha().fechaActual
    inversionVieja = Inversion.getByIId(iId)
    tasa = Tasa.getByTId(inversionVieja.tId)
    cliente = Cliente.getByCId(inversionVieja.cId)

    ganancias = inversionVieja.montoFinal - inversionVieja.montoInicial
    
    gananciasFondo = ganancias * 0.1
    gananciasActualesFondo = int(Fondo.getFondo().ganancias)
    Fondo.getFondo().updateGanancias(gananciasActualesFondo + gananciasFondo)

    montoInicial = inversionVieja.montoFinal-gananciasFondo
    montoFinal = float(montoInicial) * (float(tasa.interesTotal)/float(100)+1)
    inversionNueva = Inversion(0, cliente.cId, fechaActual, fechaActual + timedelta(days=tasa.periodoEnMeses*30), tasa.tId, montoInicial, montoFinal )
    inversionNueva.saveToDb()
    inversionVieja.deleteFromDb()

    return redirect(url_for('inversiones.getInversionesCliente', cId = cliente.cId))


@inversion_blueprint.route('sacarInversion/<string:iId>')
def sacarInversion(iId):

    fondo = Fondo.getFondo()
    iId = int(iId)
    inversion = Inversion.getByIId(iId)
    ganancias = inversion.montoFinal - inversion.montoInicial
    gananciasCliente = ganancias * 0.9
    gananciasFondo = ganancias * 0.1

    gananciasActualesFondo = int(Fondo.getFondo().ganancias)
    fondo.updateGanancias(gananciasActualesFondo + gananciasFondo)
    cliente = Cliente.getByCId(inversion.cId)
    cliente.updateSaldoVista(inversion.montoInicial + gananciasCliente)
    inversion.deleteFromDb()
    return redirect(url_for('inversiones.getInversionesCliente', cId = cliente.cId))

@inversion_blueprint.route('/crea_inversion', methods=['GET', 'POST'])
def crea_inversion():
    if request.method == 'POST':
        _id = request.form['id']
        nombre = request.form['nombre']
        periodo = request.form['periodo']
        interes = request.form['interes']

        inversion = Inversion(_id, nombre, int(periodo), int(interes)*1.0, int(interes)/365.0, int(interes)/12.0*int(periodo))

        inversion.saveToDb()
    
    fecha = Fecha.getFecha()
    return render_template("crea_inversion.jinja2", fecha=fecha)