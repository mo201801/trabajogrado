from rethinkdb import RethinkDB

r = RethinkDB()
r.connect('localhost', 28015).repl()

# Crear base de datos y tabla
try:
    r.db_create('test-divorcio').run()
except:
    pass

try:
    r.db('test-divorcio').table_create('divorcio').run()
except:
    pass

# Datos de muestra
cases_data = [
    {
        "id": 1,
        "documento": "56984758-8",
        "tipo_caso": "Divorcio",
        "encargado": "Lic. Juan Ramos",
        "fecha_creacion": "15/06/2024"
    },
    {
        "id": 2,
        "documento": "25658420-1",
        "tipo_caso": "Divorcio",
        "encargado": "Lic. Joel Fernandez",
        "fecha_creacion": "17/06/2024"
    },
    {
        "id": 3,
        "documento": "02654170-8",
        "tipo_caso": "Divorcio",
        "encargado": "Lic. Manuel Martinez",
        "fecha_creacion": "20/06/2024"
    }
]

# Insertar datos de muestra
r.db('test-divorcio').table('divorcio').insert(cases_data).run()

print("Base de datos configurada con datos de muestra.")
