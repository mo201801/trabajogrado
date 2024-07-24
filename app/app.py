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
    return render_template("clientes.html")

@app.route('/login')
def index():
	flash('An error occurred.', 'error')
	return render_template('login.html')



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


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
