from flask import Flask, render_template, jsonify
from rethinkdb import RethinkDB

app = Flask(__name__)
r = RethinkDB()

# Configurar la conexión a RethinkDB
conn = r.connect("localhost", 28015)

@app.route('/')
def traspasoVehiculo():
    return render_template('traspasoVehiculo.html')



@app.route('/data', methods=['GET'])
def get_data():
    table_name = 'documents'
    data = list(r.db('test').table(table_name).run(conn))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
