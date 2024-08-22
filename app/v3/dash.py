from rethinkdb import RethinkDB

# Conéctate a RethinkDB
r = RethinkDB()
r.connect('localhost', 28015).repl()


# Crea la base de datos
try:
    r.db_create('dashboard').run()
except:
    pass

try:
    r.db('dashboard').table_create('documentos').run()
except:
    pass


# Inserta datos de ejemplo en la tabla de documentos
cases_data = [
     {'estado': 'Borrador', 'cantidad': 52},
    {'estado': 'Aprobados', 'cantidad': 99},
    {'estado': 'Revisión', 'cantidad': 23},
    {'estado': 'Finalizado', 'cantidad': 50}
]

# Insertar datos de muestra
r.db('dashboard').table('documentos').insert(cases_data).run()


print("Base de datos y tablas creadas con éxito.")
