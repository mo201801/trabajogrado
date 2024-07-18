from rethinkdb import RethinkDB

r = RethinkDB()
r.connect('localhost', 28015).repl()

# Crear base de datos y tabla
try:
    r.db_create('test').run()
except:
    pass

try:
    r.db('test').table_create('documents').run()
except:
    pass

# Datos de muestra
cases_data = [
    {
        "id": 1,
        "documento": "56984758-8",
        "tipo_caso": "Traspaso de Vehiculo",
        "encargado": "Lic. Antonio Hernandez",
        "fecha_creacion": "14/06/2024"
    },
    {
        "id": 2,
        "documento": "25658420-1",
        "tipo_caso": "Traspaso de Vehiculo",
        "encargado": "Lic. Antonio Hernandez",
        "fecha_creacion": "13/06/2024"
    },
    {
        "id": 3,
        "documento": "02654170-8",
        "tipo_caso": "Traspaso de Vehiculo",
        "encargado": "Lic. Antonio Hernandez",
        "fecha_creacion": "16/06/2024"
    }
]

# Insertar datos de muestra
r.db('test').table('documents').insert(cases_data).run()

print("Base de datos configurada con datos de muestra.")
