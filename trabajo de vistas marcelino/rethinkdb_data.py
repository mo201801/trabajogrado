from rethinkdb import RethinkDB

r = RethinkDB()
r.connect('localhost', 28015).repl()

# Crear base de datos y tabla
try:
    r.db_create('lawfirm').run()
except:
    pass

try:
    r.db('lawfirm').table_create('cases').run()
except:
    pass

# Datos de muestra
cases_data = [
    {
        "numero_documento": "DOC009",
        "tipo_caso": "Inmuebles",
        "abogado_encargado": "Robert Lopez",
        "fecha_creacion": "2023-07-10"
    },
    {
        "numero_documento": "DOC010",
        "tipo_caso": "Inmuebles",
        "abogado_encargado": "Julia Fernanda",
        "fecha_creacion": "2023-07-11"
    },
    {
        "numero_documento": "DOC011",
        "tipo_caso": "Penal",
        "abogado_encargado": "Raul Mendez",
        "fecha_creacion": "2023-07-26"
    },
    {
        "numero_documento": "DOC012",
        "tipo_caso": "Traspaso de Vehículo",
        "abogado_encargado": "Eduardo Cruz",
        "fecha_creacion": "2023-07-09"
    }
]

# Insertar datos de muestra
r.db('lawfirm').table('cases').insert(cases_data).run()

print("Base de datos configurada con datos de muestra.")
