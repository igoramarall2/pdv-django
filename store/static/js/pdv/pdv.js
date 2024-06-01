$(document).ready(function () {
    // Limpar o carrinho no localStorage ao carregar a página
    localStorage.removeItem('carrinho');
    var carrinho = [];

    function initializeDataTable() {
        $('#produtosBuscadosTabela').DataTable({
            language: {
                url: 'https://cdn.datatables.net/plug-ins/2.0.5/i18n/pt-BR.json',
            },
            responsive: true
        });
    }

    function atualizarCarrinho() {
        $('#carrinhoTabela tbody').empty();
        var total = 0;
        carrinho.forEach(function (item, index) {
            var row = '<tr>' +
                '<td class="text-left">' + item.name + '</td>' +
                '<td class="text-left">' + item.price + '</td>' +
                '<td class="text-left">' + item.quantity + '</td>' +
                '<td class="text-left"><button class="removerItem btn btn-danger btn-sm" data-index="' + index + '">Remover</button></td>' +
                '</tr>';
            $('#carrinhoTabela tbody').append(row);
            total += item.price * item.quantity;
        });
        $('#totalCarrinho').text(total.toFixed(2));
    }

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $(document).on('click', '#btnBuscarProdutoBtn', function (e) {
        e.preventDefault();
        var formData = $('#buscarProdutoForm').serialize();

        $.ajax({
            url: '/buscar_produtos_pdv/',
            type: 'POST',
            data: formData,
            success: function (response) {
                $('#produtosBuscadosResult').empty();
                $('#produtosBuscadosResult').html(response);
                initializeDataTable();
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $(document).on('click', '.addItemsCarrinho', function (e) {
        e.preventDefault();
        var itemRow = $(this).closest('tr');
        var itemName = itemRow.find('td:eq(0)').text();
        var itemPrice = parseFloat(itemRow.find('td:eq(1)').text());
        var itemQuantity = parseInt(itemRow.find('td:eq(2) input').val());

        var itemExists = false;

        // Verificar se o item já existe no carrinho
        carrinho.forEach(function (item) {
            if (item.name === itemName) {
                item.quantity += itemQuantity;
                itemExists = true;
            }
        });

        // Se o item não existe, adicionar ao carrinho
        if (!itemExists) {
            var item = {
                name: itemName,
                price: itemPrice,
                quantity: itemQuantity
            };
            carrinho.push(item);
        }

        localStorage.setItem('carrinho', JSON.stringify(carrinho));
        atualizarCarrinho();
    });

    $(document).on('click', '.removerItem', function (e) {
        e.preventDefault();
        var itemIndex = $(this).data('index');
        carrinho.splice(itemIndex, 1);
        localStorage.setItem('carrinho', JSON.stringify(carrinho));
        atualizarCarrinho();
    });

    $('#finalizarCompraBtn').click(function () {
        // Lógica para finalizar a compra
        var total = 0;
        carrinho.forEach(function (item) {
            total += item.price * item.quantity;
        });

        $.ajax({
            url: '/finalizar_compra/',
            type: 'POST',
            data: JSON.stringify({ carrinho: carrinho, total: total }),
            contentType: 'application/json',
            headers: { 'X-CSRFToken': csrftoken },
            success: function (response) {
                carrinho = [];
                localStorage.removeItem('carrinho');
                atualizarCarrinho();
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $('#cancelarCompraBtn').click(function () {
        // Lógica para cancelar a compra
        carrinho = [];
        localStorage.removeItem('carrinho');
        atualizarCarrinho();
    });

    // Atualizar o carrinho ao carregar a página
    atualizarCarrinho();
});
