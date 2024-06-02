$(document).ready(function() {

    $('#tabelaFornecedores').DataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Portuguese-Brasil.json"
        },
        autoWidth: false,
    });
    

}); // This is the same as $(function() {});