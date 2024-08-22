# version 2 Aplicacion
---
### Procesos de API 
---
- /crearUsuario
- /eliminarUsario
- /verUsuarios

- /verTotalDocumentos/id_user
- /penales/id_user
- /inmueble/id_user
- /vehiculos/id_user

- /log

docker run -d   --name rethinkdb-remote   -p 8080:8080   -p 28015:28015   -p 29015:29015   rethinkdb rethinkdb --join 51.222.28.110:29015 --bind all
