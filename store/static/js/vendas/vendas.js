$(document).ready(function() {
    $('.tabelaVendas').DataTable({
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Portuguese-Brasil.json"
        },
        "autoWidth": false,
        lengthChange: false
    });
});