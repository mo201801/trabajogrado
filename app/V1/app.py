from flask import Flask, render_template, request, jsonify,redirect,url_for,session
from rethinkdb import RethinkDB
import json,os
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from DB import RethinkDBCRUD
import sqlite3
from datetime import datetime

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
	if 'rol' in session:
		return redirect(url_for('menuprin'))
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
		#con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
		username = request.form["username"] # con los nombres que se definio en ajax
		pas = request.form["password"]
		con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
		print(username,pas)
		res = con.get_User('usuarios',username)

		if res.items:
			pass_bool = check_password_hash(pas,res.items[0]['password'])
			if res.items[0]['password'] == res.items[0]['username']:
				return redirect(url_for('new_pass'))
		else:
			pass_bool = check_password_hash(pas,res.items[0]['password'])
			session['rol']=res.items[0]['rol']
			session['abogado']=res.items[0]['abogado']
			session['username']=res.items[0]['username']
			return redirect(url_for('menuprin'))

		# if res.items:
		# 	datos={}
		# 	datos['id']=res.items[0]['id']
		# 	datos['abogado']=res.items[0]['abogado']
		# 	datos['password']=res.items[0]['password']
		# 	datos['rol']=res.items[0]['rol']
		# 	datos['username']=res.items[0]['username']
		# 	session['rol']=res.items[0]['rol']
		# 	session['abogado']=res.items[0]['abogado']
		# 	session['username']=res.items[0]['username']
		# 	print(datos)
		# 	admin=res.items[0]['rol']
		# 	return redirect(url_for('menuprin'))
		# else:
		# 	return redirect(url_for('index'))

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


@app.route('/NODATA')
def nodata():
	data={}
	return data


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

@app.route('/logs')
def logs():
    return render_template("logs.html")

@app.route('/new_pass')
def new_pass():
    return render_template("newpass.html") 



# ver datos en datable de logs
@app.route('/data')
def data():
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_All_Data('logs')
	data = list(res)
	return jsonify(data)



@app.route('/menuprin')
def menuprin():
	return render_template("menuprin.html")

# deslogue al usuario borra variable session
@app.route('/logout')
def logout():
	session.pop('rol',None)
	session.pop('abogado',None)
	return redirect(url_for('index'))

@app.route('/insertuser',methods=["POST"])
def insertuser():
	if request.method == 'POST':
		con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
		name = request.form["nombre"] # con los nombres que se definio en ajax
		pas = request.form["password"]
		bol_admin = request.form["admin"]
		bol_abogado = request.form["abogado"]
		
		pass_hash = generate_password_hash(pas)

		dir_regimen = f"casos/{name}/regimen"
		dir_traspasos = f"casos/{name}/traspasos"
		dir_penal = f"casos/{name}/penal"
		dir_default = [dir_regimen,dir_traspasos,dir_penal]

		for carpet in dir_default:
			os.makedirs(carpet,exist_ok=True)
			
		# insercion de datos en DB con clase
		con.insert('usuarios',{'username':name,'password':pass_hash,'rol':bol_admin,'abogado':bol_abogado})

	return redirect(url_for('index')) #,201 si queremos poner que tipo retorna


#Jesse_15/08/2024

@app.route('/subir',methods=['GET'])
def subir():
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	clientes = con.get_All_Data('clientes')
	tipo_doc = con.get_All_Data('tipo_docu')
	abogado_resp = con.get_All_Data('abo_user')
	mostr_cliente = list(clientes)
	mostr_doc = list(tipo_doc)
	mostr_abo = list(abogado_resp)
	cant_datos = len(mostr_cliente)
	dato=dict()
	for j in range(len(mostr_cliente)):
		dato[mostr_cliente[j]['Nombre']]=mostr_cliente[j]['Apellido']

	return render_template('subir.html',mostrar=dato,docu=mostr_doc,abogado=mostr_abo)

@app.route('/clientes',methods=['POST'])
def clientes():
	if request.method =='POST':
		nombre=request.form["nombre"]
		apellido=request.form["apellido"]
		telefono=request.form["tel"]
		direccion=request.form["direc"]
		fecha_nac=request.form["fena"]
		genero=request.form["gen"]
		fecha_ingre=request.form["feingre"]
		motivo_caso=request.form["motica"]
		dui=request.form["dui"]
		tel_refe=request.form["telre"]
		nom_refe=request.form["nomrefe"]
		datos={"Nombre":nombre, "Apellido":apellido, "Telefono":telefono, "Direccion":direccion,\
		"Fecha_nac":fecha_nac, "Genero":genero, "Fecha_ing":fecha_ingre, "Moti_cas":motivo_caso, "DUI":dui, "Tel_refe":tel_refe,\
		"Nomb_refe":nom_refe}
		con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
		res = con.insert('clientes', datos)
		return jsonify(datos)




if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0',debug=True)
