#-----------------------------------------------------------------------------------------------------------
# --------------APLICACION TRABAJO DE GRADO, TITULO EN CIENCIAS DE LA COMPUTACION--------------------------
# ----------------------------------------------------------------------------------------------------------
#
# Autores: Rafael Osorio,
# Fecha: Julio,Agosto 2024
#----------------------------------------------------------------------------------------------------------


from flask import Flask, render_template, request, jsonify
from rethinkdb import RethinkDB
from config_clientes import RETHINKDB_HOST, RETHINKDB_PORT, RETHINKDB_DB, RETHINKDB_TABLE
import json
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime

# espacio de carpetas de almacenamiento
#  de momento temporales debe hacerse de manera dinamica
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt','pdf'}

r = RethinkDB()
conn = r.connect(host=RETHINKDB_HOST, port=RETHINKDB_PORT, db=RETHINKDB_DB).repl()

app = Flask(__name__)
app.secret_key = 'UPE@2024_TE$15'

# espacio de almacenamiento , debe crearse primer con mkdi -p _nombre_carpeta_
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# funcion para delimitar los archivos que son admitidos.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	ip = request.remote_addr
	date= datetime.now()
	fecha = date.strftime('%Y-%m-%d')
	hora = date.strftime('%H:%M')
	msj = f'Usuario con IP: {ip} se logueo'
	servicio = 'debug'
	con.insert('logs',{'Fecha':fecha,'Hora':hora,'mensaje':msj,'servicio':servicio})
	return render_template("index.html")

@app.route('/login',methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        return redirect(url_for('creausua'))

    return render_template("loguear.html")



# hash sobre contrasenas , este metodo solo realiza hash no ingresa a DB
#Rafael-23-07-2024
@app.route('/login',methods=["POST"])
def login():
	name = request.form["nombre"] # con los nombres que se definio en ajax
	pas = request.form["password"]
	pass_hash = generate_password_hash(pas)

	print(name,pass_hash)
	#flash('An error occurred.', 'error')
	return jsonify({'Funcionamiento':pass_hash}) #,201 si queremos poner que tipo retorna

#Jesse_18/07/2024
#Eviar datos de clientes
@app.route('/clientes',methods=['POST'])
def login(): 
    if request.method =='POST':
        nom=request.form["nombre"]
        ape=request.form["apellido"]
        t=request.form["tel"]
        d=request.form["direc"]
        f=request.form["fena"]
        g=request.form["gen"]
        fi=request.form["feingre"]
        m=request.form["motica"]
        p=request.form["dui"]
        te=request.form["telre"]
        nfe=request.form["nomrefe"]
        datos=[nom,ape,t,d,f,g,fi,m,p,te,nfe]
        x=r.table('registro').insert({"Nombre":nom, "Apellido":ape, "Telefono":t, "Direccion":d,\
            "Fecha_nac":f, "Genero":g, "Fecha_ing":fi, "Moti_cas":m, "DUI":p, "Tel_refe":te,\
            "Nomb_refe":nfe}).run(conn)
    return jsonify(datos)

#Rafael_22/07/2024
#Enviar datos de cargar documentos
@app.route('/cargar',methods=['POST'])
def docu():
    if 'file' not in request.files:

        return jsonify({'message': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        print('no archivo select')
        return jsonify({'message': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Recoger otros datos del formulario
        additional_data = request.form.to_dict()
        
        # Puedes realizar más acciones con los datos adicionales aquí
        print(additional_data)
        #retorna
#{'clientes': 'rafael', 'tipo_documento': 'Contrato', 
# 'abogado': 'Juan', 'fecha_ingreso': '2024-07-25', 'comentario': 'comentario'}
        return jsonify({'message': 'File successfully uploaded', 'data': additional_data})   
    return jsonify({'message': 'File not allowed'})


#Jesse_26/07/2024
@app.route('/mostrar',methods=['GET'])
def mostrar():
    res = con.get_All_Data('registro')
    mostr_cliente = list(res)
    cant_datos = len(mostr_cliente) 
    dato=dict()
    for j in range(len(mostr_cliente)):
      dato[mostr_cliente[j]['Nombre']]=mostr_cliente[j]['Apellido']

    return render_template('mostrar.html',mostrar=dato)


#Marcelino_26/07/2024
# Muestra la info de la datatable
@app.route('/data', methods=['GET'])
def get_data():
    table_name = 'cases'
    data = list(r.db('lawfirm').table(table_name).run(conn))
    return jsonify(data)

#Marcelino_30/07/2024
# Muestra la data que esta en el dashboard, es de corregir que datos vamos a mostrar 
conn = r.connect(db='dashboard')

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

@app.route('/data/documentos')
def data_documentos():
    documentos = list(r.table('documentos').run(conn))
    return jsonify(documentos)

@app.route('/data/usuarios')
def data_usuarios():
    usuarios = list(r.table('usuarios').run(conn))
    return jsonify(usuarios)
	
#Marcelino_02/08/2024	
#Sirve para mostrar los datos en el grafico y cuadros del dashboard
@app.route('/')
def index():
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
    return render_template('dashboard.html',target=data)



#Jesse_02/08/2024
#Sirve para la aplicacion de roles de usuario
@app.route('/vista/<usuario>')
def vista(usuario):
    f=con.get_User('rol', usuario)
    t=f.items[0]['rol']
    return render_template("roles.html", datavis=t)


@app.route('/document/<informacion>')
def vista2(informacion):
    print(informacion)
    x=informacion*2
    return str(x)


#Jesse_03/08/2024
#funciones para las rutas de vistas

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

@app.route('/inise')
def inise():
    return render_template("loguear.html")

#Marcelino_11_08_24
#Dashboard con datatable para mostrar tabla de usuario
@app.route('/get_data')
def get_data():
    con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
    res = con.get_All_Data('resumen_usuario')
    data = list(res)
    return jsonify(data)

#Marcelino_12_08_24
#Dashboard con datatable para mostrar tabla de cargar documentos
@app.route('/get_documentos')
def get_documentos():
    con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
    res = con.get_All_Data('resumen_documentos')
    data = list(res)
    return jsonify(data)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
