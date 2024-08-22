$(document).ready(function() {
    $('#documentsTable').DataTable({
        "ajax": "/api/lawfirm",
        "columns": [
            { "data": "numero_documento" },
            { "data": "tipo_caso" },
            { "data": "abogado_encargado" },
            { "data": "fecha_creacion" }
        ]
    });
});