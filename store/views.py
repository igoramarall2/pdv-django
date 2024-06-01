from django.shortcuts import render
from .models import Cliente, Produto, Categoria, Vendas, VendaProduto
from django.db.models import Count, Sum, Q
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def index(request):
    total_produtos = Produto.objects.count()
    total_categorias = Categoria.objects.count()
    total_vendas = Vendas.objects.count()

    # Dados para o gráfico de vendas mensais
    sales_data = Vendas.objects.extra(select={'month': 'strftime("%%m", data_venda)'}).values('month').annotate(total=Sum('total')).order_by('month')
    sales_months = json.dumps([item['month'] for item in sales_data], cls=DecimalEncoder)
    sales_totals = json.dumps([item['total'] for item in sales_data], cls=DecimalEncoder)

    # Dados para o gráfico de vendas por produto
    product_sales_data = VendaProduto.objects.values('produto__nome').annotate(total=Sum('quantidade')).order_by('produto__nome')
    product_labels = json.dumps([item['produto__nome'] for item in product_sales_data])
    product_sales_totals = json.dumps([item['total'] for item in product_sales_data], cls=DecimalEncoder)

    # Dados para o gráfico de vendas diárias
    daily_sales_data = Vendas.objects.extra(select={'day': 'strftime("%%Y-%%m-%%d", data_venda)'}).values('day').annotate(total=Sum('total')).order_by('day')
    daily_sales_dates = json.dumps([item['day'] for item in daily_sales_data], cls=DecimalEncoder)
    daily_sales_totals = json.dumps([item['total'] for item in daily_sales_data], cls=DecimalEncoder)

    context = {
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'total_vendas': total_vendas,
        'sales_months': sales_months,
        'sales_totals': sales_totals,
        'product_labels': product_labels,
        'product_sales_totals': product_sales_totals,
        'daily_sales_dates': daily_sales_dates,
        'daily_sales_totals': daily_sales_totals,
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
    nome = request.POST.get("buscaProdutoNome")
    categoria = request.POST.get("buscaProdutoCategoria")

    Q_produtos = Q()
    if nome:
        Q_produtos &= Q(nome__icontains=nome)
    if categoria:
        Q_produtos &= Q(categoria__nome__icontains=categoria)

    produtos = Produto.objects.filter(Q_produtos, estoque_disp=True)
    context = {"produtos": produtos}
    
    return render(request, "store/pdv/produtos_buscados.html", context)