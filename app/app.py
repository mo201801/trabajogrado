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

r = RethinkDB()
conn = r.connect(host=RETHINKDB_HOST, port=RETHINKDB_PORT, db=RETHINKDB_DB).repl()

app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template("clientes.html")


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

#Jesse_18/07/2024
#Eviar datos de cargar documentos
@app.route('/cargar',methods=['POST'])
def docu(): 
    if request.method =='POST':
        secli=request.form["clientes"]
        ti=request.form["tipdoc"]
        a=request.form["abo"]
        fi=request.form["feingre"]
        c=request.form["coment"]
        prueba=[secli,ti,a,fi,c]
        print(prueba);
        p=r.table('cargadoc').insert({"Nom_Cliente":secli, "Tipo_doc":ti, "Agogado":a, "Fecha_Ing":fi,\
            "Comentario":c}).run(conn)
    return jsonify(prueba)





if __name__ == '__main__':
    app.run(debug=True)
