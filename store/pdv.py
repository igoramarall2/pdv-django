from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vendas, VendaProduto, Produto, Cliente
import json

@csrf_exempt
def finalizar_compra(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        carrinho = data.get('carrinho', [])
        total = data.get('total', 0)

        # Supondo que você tenha um cliente padrão ou esteja obtendo o cliente de alguma forma

        venda = Vendas.objects.create(total=total)

        for item in carrinho:
            produto = Produto.objects.get(nome=item['name'])
            quantidade = item['quantity']
            subtotal = produto.preco * quantidade
            VendaProduto.objects.create(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                subtotal=subtotal
            )

        return JsonResponse({'message': 'Compra finalizada com sucesso.'})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)