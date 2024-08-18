from flask import Flask, render_template, request, jsonify,redirect,url_for,session
from rethinkdb import RethinkDB
import json,os
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from DB import RethinkDBCRUD
import sqlite3
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'UPE@2024_TE$15'




@app.route('/api/insert/clientes', methods=['POST'])
def insert_cliente():
	# Obtén los datos del formulario enviados en la solicitud
	data = request.json
	cliente = {
	'nombre': data['nombre'],
	'apellidos': data['apellidos'],
	'telefono': data['telefono'],
	'direccion': data['direccion'],
	'fecha_nacimiento': data['fecha_nacimiento'],
	'genero': data['genero'],
	'fecha_ingreso': data['fecha_ingreso'],
	'motivo': data['motivo'],
	'dui': data['dui'],
	'telefono_referencia': data['telefono_referencia'],
	'nombre_referencia': data['nombre_referencia']
	}
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	con.insert('clientes',{'nombre':cliente['nombre'],'apellidos':cliente['apellidos'],'telefono':cliente['telefono'],\
		'direccion':cliente['direccion'],'fecha_nacimiento':cliente['fecha_nacimiento'],'genero':cliente['genero'],\
		'fecha_ingreso':cliente['fecha_ingreso'],'motivo':cliente['motivo'],'dui':cliente['dui'],'telefono_referencia':cliente['telefono_referencia'],\
		'nombre_referencia':cliente['nombre_referencia']})
	return jsonify(cliente), 201

@app.get('/api/get/clientes/<id_cliente>')
def get_clientes(id_cliente):
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_dui('clientes', id_cliente)
	data = list(res)
	return jsonify(data)


#Metodo para eliminar por medio del campo ID un usuario
@app.get('/api/delete/clientes/<id_eliminar>')
def delete_clientes(id_eliminar):
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.delete('clientes', id_eliminar)
	mensaje = f"Usuario {id_eliminar} eliminado correctamente"
	return jsonify(mensaje)


@app.post('/api/update/clientes/<id_update>')
def update_clientes(id_update):
	# Retorna todos los clientes almacenados
	data = request.json
	cliente = {
	'nombre': data['nombre'],
	'apellidos': data['apellidos'],
	'telefono': data['telefono'],
	'direccion': data['direccion'],
	'fecha_nacimiento': data['fecha_nacimiento'],
	'genero': data['genero'],
	'fecha_ingreso': data['fecha_ingreso'],
	'motivo': data['motivo'],
	'dui': data['dui'],
	'telefono_referencia': data['telefono_referencia'],
	'nombre_referencia': data['nombre_referencia']
	}
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	con.update('clientes', id_update,{'nombre':cliente['nombre'],'apellidos':cliente['apellidos'],'telefono':cliente['telefono'],\
		'direccion':cliente['direccion'],'fecha_nacimiento':cliente['fecha_nacimiento'],'genero':cliente['genero'],\
		'fecha_ingreso':cliente['fecha_ingreso'],'motivo':cliente['motivo'],'dui':cliente['dui'],'telefono_referencia':cliente['telefono_referencia'],\
		'nombre_referencia':cliente['nombre_referencia']})
	mensaje = f"Cliente {id_update} actualizado correctamente"
	return jsonify(mensaje)



@app.post('/api/insertuser')
def agregar_usuario():
	if request.method == 'POST':
		con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
		data = request.json
		usuario = {
		'nombre': data['nombre'],
		'password': data['password'],
		'admin': data['admin'],
		'abogado': data['abogado'],
		'cant_login': data['cant_login']
		}
		pass_hash = generate_password_hash(usuario['password'])

		dir_regimen = f"casos/{usuario['nombre']}/regimen"
		dir_traspasos = f"casos/{usuario['nombre']}/traspasos"
		dir_penal = f"casos/{usuario['nombre']}/penal"
		dir_default = [dir_regimen,dir_traspasos,dir_penal]

		for carpet in dir_default:
			os.makedirs(carpet,exist_ok=True)
			
		# insercion de datos en DB con clase
		con.insert('usuarios',{'username':usuario['nombre'],'password':pass_hash,'rol':usuario['admin'],'abogado':usuario['abogado'],'cant_login':usuario['cant_login']})

	return jsonify('Usuario ingresado') #,201 si queremos poner que tipo retorna


@app.get('/api/delete/usuario/<id_deleteuser>')
def delete_usuario(id_deleteuser):
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.delete('usuarios', id_deleteuser)
	mensaje = f"Usuario {id_deleteuser} eliminado correctamente"
	return jsonify(mensaje)


@app.get('/api/get/usuario')
def get_usuario():
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_All_Data('usuarios')
	data = list(res)
	return jsonify(data)


@app.get('/api/get/documentos')
def get_documentos():
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_All_Data('documentos')
	data = list(res)
	return jsonify(data)


@app.get('/api/get/penales/<id_user>')
def get_penales(id_user):
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_User('caso_penal', id_user)
	data = list(res)
	return jsonify(data)

@app.get('/api/get/inmueble/<id_user>')
def get_inmueble(id_user):
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_User('caso_inmuebles', id_user)
	data = list(res)
	return jsonify(data)

@app.get('/api/get/vehiculos/<id_user>')
def get_vehiculos(id_user):
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_User('caso_vehiculo', id_user)
	data = list(res)
	return jsonify(data)

@app.get('/api/get/logs')
def get_logs():
	# Retorna todos los clientes almacenados
	con = RethinkDBCRUD(host='51.222.28.110',db='DB_UPES')
	res = con.get_All_Data('logs')
	data = list(res)
	return jsonify(data)


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)



