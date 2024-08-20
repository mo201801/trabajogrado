from flask import Flask, render_template, request, jsonify,redirect,url_for,session
from rethinkdb import RethinkDB
import json,os
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from DB import RethinkDBCRUD
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename

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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/cargar', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        additional_data = request.form.to_dict()
        print(additional_data)

        if 'archivo' not in request.files:
            return jsonify({'message': 'No file part'}), 400
        
        file = request.files['archivo']
        
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Recoger otros datos del formulario
            print(additional_data)
            
            # Puedes realizar más acciones con los datos adicionales aquí
            
            return jsonify({'message': 'File successfully uploaded', 'data': additional_data}), 200
        
        return jsonify({'message': 'File not allowed'}), 400


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
	servicio = 'info'
	con.insert('logs',{'Fecha':fecha,'Hora':hora,'Mensaje':msj,'Servicio':servicio})
	return render_template("index.html")




@app.route('/login',methods=['GET', "POST"])
def login():
	if request.method == 'POST':
		conlite = sqlite3.connect('ingresos.db')
		curlite = conlite.cursor()

		con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
		username = request.form["username"] # con los nombres que se definio en ajax
		pas = request.form["password"]
		res = con.get_User('usuarios',username)

		if res.items:
			pass_bool = check_password_hash(res.items[0]['password'],pas)
		
		retorno =False


		if pass_bool:
			sql ='''select * from ingresos where username=?'''
			curlite.execute(sql,(username,))
			fila = curlite.fetchone()
			if fila is None:
				retorno =False
				print('no hay user')
				conlite.close()
			else:

				retorno=True
				print('total de ingresos',fila[2])
				conlite.close()
				if fila[2]==0:
					return render_template("newpass.html",user=fila[1])


		if pass_bool and retorno:
				return jsonify('todo ok') #redirect(url_for('new_pass'))
		else:
			# pass_bool = check_password_hash(pas,res.items[0]['password'])
			# session['rol']=res.items[0]['rol']
			# session['abogado']=res.items[0]['abogado']
			# session['username']=res.items[0]['username']
			return jsonify('algo salio mal') #redirect(url_for('index'))

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



@app.route('/vehiculo')
def vehiculo():
	return render_template("vehiculo.html")

@app.route('/inmueble')
def inmueble():
	return render_template("inmueble.html")

@app.route('/penal')
def penal():
	return render_template("penal.html")

@app.route('/menuprin')
def menuprin():
	return render_template("menuprin.html")


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

@app.route('/clientes')
def clientes():
    return render_template("clientes.html")

# ver datos en datable de logs
@app.route('/data')
def data():
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_All_Data('logs')
	data = list(res)
	return jsonify(data)





# deslogue al usuario borra variable session
@app.route('/logout')
def logout():
	session.pop('rol',None)
	session.pop('abogado',None)
	return redirect(url_for('index'))

@app.route('/insertuser',methods=["POST"])
def insertuser():
	if request.method == 'POST':
		conlite = sqlite3.connect('ingresos.db')
		curlite = conlite.cursor()


		con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
		name = request.form["nombre"] # con los nombres que se definio en ajax
		pas = request.form["password"]
		bol_admin = request.form["admin"]
		bol_abogado = request.form["abogado"]
		
		pass_hash = generate_password_hash(pas)

		sql ='''insert into ingresos(username) values(?)'''
		curlite.execute(sql,(name,))
		conlite.commit()

		dir_regimen = f"casos/{name}/regimen"
		dir_traspasos = f"casos/{name}/traspasos"
		dir_penal = f"casos/{name}/penal"
		dir_default = [dir_regimen,dir_traspasos,dir_penal]

		conlite.close()


		for carpet in dir_default:
			os.makedirs(carpet,exist_ok=True)
			
		# insercion de datos en DB con clase
		con.insert('usuarios',{'username':name,'password':pass_hash,'rol':bol_admin,'abogado':bol_abogado})

	return redirect(url_for('mprincipal')) #,201 si queremos poner que tipo retorna




#-----------------------------------------------------------------------
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

#Marcelino_14_08_24
#Mejoras en la vista categorias, vehiculo, penal e inmuebles
#funcion para menuprincipal y que trabaje el datatable
@app.route('/mprincipal')
def mprincipal():
    con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
    res = con.get_All_Data('documentos')
    data = list(res)
    return jsonify(data)

#funcon para la vista de categoria penal
@app.route('/cpenal')
def cpenal():
    con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
    res = con.get_All_Data('caso_penal')
    data = list(res)
    return jsonify(data)

#funcon para la vista de categoria inmuebles
@app.route('/inmuebles')
def inmuebles():
    con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
    res = con.get_All_Data('caso_inmuebles')
    data = list(res)
    return jsonify(data)

#funcon para la vista de categoria vehiculo
@app.route('/traspaso')
def traspaso():
    con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
    res = con.get_All_Data('caso_vehiculo')
    data = list(res)
    return jsonify(data)

@app.route('/clientes',methods=['POST'])
def rclientes():
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
		datos={"nombre":nombre, "apellidos":apellido, "telefono":telefono,\
		"direccion":direccion,\
		"fecha_nacimiento":fecha_nac, "genero":genero, "fecha_ingreso":fecha_ingre, \
		"motivo":motivo_caso, 'dui':dui, "telefono_referencia":tel_refe,\
		"nombre_referencia":nom_refe}
		con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
		res = con.insert('clientes', datos)
		return jsonify(datos)


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

#Jesse_19/08/2024
@app.route('/buscar')
def buscar():
    return render_template("buscar.html")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0',debug=True)
