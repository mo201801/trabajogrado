from flask import Flask, render_template, request, jsonify
from rethinkdb import RethinkDB
from config_clientes import RETHINKDB_HOST, RETHINKDB_PORT, RETHINKDB_DB, RETHINKDB_TABLE
import json
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from DB import RethinkDBCRUD
con = RethinkDBCRUD(host='51.222.28.110', db='user')  

# espacio de carpetas de almacenamiento
#  de momento temporales debe hacerse de manera dinamica
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt','pdf'}


app = Flask(__name__)
app.secret_key = 'UPE@2024_TE$15'

# espacio de almacenamiento , debe crearse primer con mkdi -p _nombre_carpeta_
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# funcion para delimitar los archivos que son admitidos.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index(): 
    return render_template("clientes.html")

@app.route('/inise')
def inise():
    return render_template("loguear.html")

    
#Marcelino_02/08/2024   
#Sirve para mostrar los datos en el grafico y cuadros del dashboard
@app.route('/dashboard')
def dashboard():
    hora=datetime.now()
    h=hora.strftime('%Y')
    d=hora.strftime('%d')
    m=hora.strftime('%m')
    s=hora.strftime('%s')
    data={}
    data['borrador']=h
    data['aprobado']=d
    data['revision']=m
    data['finalizado']=s
    return render_template("dashboard.html",target=data)



@app.route('/traspaso')
def traspaso():
    return render_template("traspasoVehiculo.html")


@app.route('/inmueble')
def inmueble():
    return render_template("herencia.html")

@app.route('/penal')
def penal():
    return render_template("penal.html")


@app.route('/subir')
def subir():
    return render_template("subir.html")

@app.route('/editar')
def editar():
    return render_template("documento.html")


@app.route('/creausua')
def creausua():
    return render_template("creausua.html")

@app.route('/estadistica')
def estadistica():
    return render_template("logs.html")


@app.route('/menuprin')
def menuprin():
    return render_template("menuprin.html")





if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)