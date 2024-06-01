from django.shortcuts import render
from .models import Cliente, Produto, Categoria, Vendas
from django.db.models import Count, Sum, Q
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def index(request):
    total_clientes = Cliente.objects.count()
    total_produtos = Produto.objects.count()
    total_categorias = Categoria.objects.count()
    total_vendas = Vendas.objects.count()

    # Dados para o gráfico de vendas mensais
    sales_data = Vendas.objects.extra(select={'month': 'strftime("%%m", data_venda)'}).values('month').annotate(total=Sum('total')).order_by('month')
    sales_months = json.dumps([item['month'] for item in sales_data], cls=DecimalEncoder)
    sales_totals = json.dumps([item['total'] for item in sales_data], cls=DecimalEncoder)

    # Dados para o gráfico de distribuição de produtos por categoria
    category_data = Produto.objects.values('categoria__nome').annotate(total=Count('id')).order_by('categoria__nome')
    category_labels = json.dumps([item['categoria__nome'] for item in category_data])
    category_totals = json.dumps([item['total'] for item in category_data], cls=DecimalEncoder)

    context = {
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'total_vendas': total_vendas,
        'sales_months': sales_months,
        'sales_data': sales_totals,
        'category_labels': category_labels,
        'category_data': category_totals,
    }

    return render(request, 'store/index.html', context)


def cadastros(request):
    categorias = Categoria.objects.all()
    context = {"categorias": categorias}
    return render(request, "store/cadastros/cadastros.html", context)


def estoque(request):
    estoque = Produto.objects.all()
    context = {
        "estoque": [
            {
                "nome": p.nome,
                "descricao": p.descricao,
                "preco": p.preco,
                "estoque_qntd": p.estoque_qntd,
                "categoria": p.categoria.nome,
            }
            for p in estoque
        ]
    }
    return render(request, "store/estoque/estoque.html", context)


def pdv(request):
    return render(request, "store/pdv/pdv.html")


def buscar_produtos_pdv(request):
    codigo = request.POST.get("buscaProdutoCodigo")
    nome = request.POST.get("buscaProdutoNome")
    categoria = request.POST.get("buscaProdutoCategoria")

    produtos = None
    if codigo or nome or categoria:
        # if codigo:
        #     Q_produtos = Q(codigo=codigo)
        if nome:
            Q_produtos = Q(nome__icontains=nome)
        if categoria:
            Q_produtos = Q_produtos & Q(categoria__icontains=categoria)

        produtos = Produto.objects.filter(Q_produtos)
        context = {"produtos": produtos}
    else:
        produtos = Produto.objects.all()
        context = {"produtos": produtos}
    
    return render(request, "store/pdv/produtos_buscados.html", context)

