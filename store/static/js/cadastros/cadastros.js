$( document ).ready(function() {

    $('#cadastroClientes').on('click', function() {
        event.preventDefault(); // Prevent default form submission
        var formData = $('#clienteForm').serialize();
        formData += '&csrfmiddlewaretoken=' + $('[name=csrfmiddlewaretoken]').val(); // Include CSRF token
        // Now you can process formDataArray as needed
        // console.log(formData);

        $.ajax({
            url: '/cadastros_clientes/',
            type: 'POST',
            data: formData,
            success: function(data) {
                if (data['message'] == 'Cadastro com Sucesso') {
                    alert(data['message']);
                }
                
                $('#clienteForm').trigger("reset");
            },
            error: function(data) {
                console.log(data);
                alert('Erro ao cadastrar cliente!');
            }
        });
    });

    $('#cadastroCategorias').on('click', function() {
        event.preventDefault(); // Prevent default form submission
        var formData = $('#categoriaForm').serialize();
        // Now you can process formDataArray as needed
        // console.log(formData);

        $.ajax({
            url: '/cadastro_categorias/',
            type: 'POST',
            data: formData,
            success: function(data) {
                if (data['message'] == 'Cadastro com Sucesso') {
                    alert(data['message']);
                }
                
                $('#categoriaForm').trigger("reset");
            },
            error: function(data) {
                console.log(data);
                alert('Erro ao cadastrar categoria!');
            }
        });

    });

    
    $('#cadastroProdutos').on('click', function() {
        event.preventDefault(); // Prevent default form submission
        var formData = $('#produtoForm').serialize();
        // Now you can process formDataArray as needed
        // console.log(formData);

        $.ajax({
            url: '/cadastro_produtos/',
            type: 'POST',
            data: formData,
            success: function(data) {
                if (data['message'] == 'Cadastro com Sucesso') {
                    alert(data['message']);
                }
                
                $('#produtoForm').trigger("reset");
            },
            error: function(data) {
                console.log(data);
                alert('Erro ao cadastrar produto!');
            }
        });

    });

    $('#cadastroMateriasPrimas').on('click', function() {
        event.preventDefault(); // Prevent default form submission
        var formData = $('#materiaPrimaForm').serialize();
        console.log(formData);
        formData += '&csrfmiddlewaretoken=' + $('[name=csrfmiddlewaretoken]').val(); // Include CSRF token
        // Now you can process formDataArray as needed
        // console.log(formData);

        $.ajax({
            url: '/cadastro_materias_primas/',
            type: 'POST',
            data: formData,
            success: function(data) {
                if (data['message'] == 'Cadastro com Sucesso') {
                    alert(data['message']);
                }
                
                $('#materiaPrimaForm').trigger("reset");
            },
            error: function(data) {
                console.log(data);
                alert('Erro ao cadastrar produto!');
            }
        });

    });

    $('#cadastroFornecedores').on('click', function() {
        event.preventDefault(); // Prevent default form submission
        var formData = $('#fornecedorForm').serialize();
        console.log(formData);
        formData += '&csrfmiddlewaretoken=' + $('[name=csrfmiddlewaretoken]').val(); // Include CSRF token
        // Now you can process formDataArray as needed
        // console.log(formData);

        $.ajax({
            url: '/cadastro_fornecedores/',
            type: 'POST',
            data: formData,
            success: function(data) {
                if (data['message'] == 'Cadastro com Sucesso') {
                    alert(data['message']);
                }
                
                $('#fornecedorForm').trigger("reset");
            },
            error: function(data) {
                console.log(data);
                alert('Erro ao cadastrar produto!');
            }
        });

    });







    $('#catProd').select2({
        placeholder: 'Selecione uma categoria',
        theme:"bootstrap-5"
    });
    $('#fornecedorMat').select2({
        placeholder: 'Selecione um fornecedor',
        theme:"bootstrap-5"
    });


});