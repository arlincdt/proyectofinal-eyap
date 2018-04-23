from flask import Flask, render_template, session, redirect, request, url_for
import requests
import os
from src.common.database import Database
from src.models.fondo import Fondo
from src.models.tasa import Tasa
from src.models.clientes.cliente import Cliente
from src.models.fechas.fecha import Fecha
from src.models.inversiones.inversion import Inversion
from src.models.promotores.promotor import Promotor

__author__ = "edlgg"

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = os.environ.get("SECRET_KEY")

@app.before_first_request
def init_db():
	#Database.initialize(minconn=1, maxconn=10, user="edlgg", password="6627982", host="localhost", database="postgres")
    Database.initialize(minconn=1, maxconn=10, user=os.environ.get("USER"), password=os.environ.get("PASSWORD"), host=os.environ.get("HOST"), database=os.environ.get("DATABASE"))
    #Database.initialize(minconn=1, maxconn=10, user="hlimerijutaovb", password="c29a71ef6c0a58c415488e2d18a49bdbe2002a86d92e0fb28082fa41d7ddec49", host="ec2-23-21-217-27.compute-1.amazonaws.com", database="de4s7mkdh74efr")

@app.route('/')
def home():
    fecha = Fecha.getFecha()
    return render_template('home.jinja2', fecha = fecha)

from src.models.promotores.views import promotor_blueprint
from src.models.clientes.views import cliente_blueprint
from src.models.fechas.views import fecha_blueprint
from src.models.inversiones.views import inversion_blueprint
app.register_blueprint(promotor_blueprint, url_prefix="/promotores")
app.register_blueprint(cliente_blueprint, url_prefix="/clientes")
app.register_blueprint(fecha_blueprint, url_prefix="/fechas")
app.register_blueprint(inversion_blueprint, url_prefix="/inversiones")
