from django.shortcuts import render
from .models import Cliente, Produto, Categoria, Vendas, VendaProduto
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from django.utils import timezone
import json
from datetime import datetime, timedelta
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
    periodo = request.GET.get("periodo", "Hoje")
    agora = timezone.now()  # Usar timezone.now() em vez de datetime.now()

    if periodo == "Hoje":
        inicio_periodo = agora - timedelta(days=1)
    elif periodo == "7 dias":
        inicio_periodo = agora - timedelta(days=7)
    elif periodo == "15 dias":
        inicio_periodo = agora - timedelta(days=15)
    elif periodo == "30 dias":
        inicio_periodo = agora - timedelta(days=30)
    elif periodo == "90 dias":
        inicio_periodo = agora - timedelta(days=90)
    elif periodo == "180 dias":
        inicio_periodo = agora - timedelta(days=180)
    elif periodo == "365 dias":
        inicio_periodo = agora - timedelta(days=365)
    else:
        inicio_periodo = agora - timedelta(days=1)  # Default to Hoje

    # Filtrar vendas pelo período selecionado
    vendas_filtradas = Vendas.objects.filter(data_venda__gte=inicio_periodo)

    # Atualize os dados para os gráficos com base nas vendas filtradas
    sales_data = (
        vendas_filtradas.extra(select={"month": 'strftime("%%m", data_venda)'})
        .values("month")
        .annotate(total=Sum("total"))
        .order_by("month")
    )
    sales_months = json.dumps(
        [item["month"] for item in sales_data], cls=DecimalEncoder
    )
    sales_totals = json.dumps(
        [item["total"] for item in sales_data], cls=DecimalEncoder
    )

    # Dados para o gráfico de vendas por produto
    product_sales_data = (
        VendaProduto.objects.filter(venda__in=vendas_filtradas)
        .values("produto__nome")
        .annotate(total=Sum("quantidade"))
        .order_by("produto__nome")
    )
    product_labels = json.dumps(
        [f"{item['produto__nome'][:12]}..." for item in product_sales_data]
    )
    product_sales_totals = json.dumps(
        [item["total"] for item in product_sales_data], cls=DecimalEncoder
    )

    # Dados para o gráfico de vendas diárias
    daily_sales_data = (
        vendas_filtradas.extra(select={"day": 'strftime("%%Y-%%m-%%d", data_venda)'})
        .values("day")
        .annotate(total=Sum("total"))
        .order_by("day")
    )
    daily_sales_dates = json.dumps(
        [item["day"] for item in daily_sales_data], cls=DecimalEncoder
    )
    daily_sales_totals = json.dumps(
        [item["total"] for item in daily_sales_data], cls=DecimalEncoder
    )

    # Dados para o gráfico de vendas por categoria
    category_sales_data = (
        VendaProduto.objects.filter(venda__in=vendas_filtradas)
        .values("produto__categoria__nome")
        .annotate(total=Sum("quantidade"))
        .order_by("produto__categoria__nome")
    )
    category_labels = json.dumps(
        [item["produto__categoria__nome"] for item in category_sales_data]
    )
    category_sales_totals = json.dumps(
        [item["total"] for item in category_sales_data], cls=DecimalEncoder
    )

    # Dados para a soma total da quantidade de produtos em estoque por categoria
    stock_data = (
        Produto.objects.values("categoria__nome")
        .annotate(total_stock=Sum("estoque_qntd"))
        .order_by("categoria__nome")
    )
    stock_labels = json.dumps([item["categoria__nome"] for item in stock_data])
    stock_totals = json.dumps(
        [item["total_stock"] for item in stock_data], cls=DecimalEncoder
    )

    # Estoque total
    total_stock = Produto.objects.aggregate(total_stock=Sum("estoque_qntd"))[
        "total_stock"
    ]

    context = {
        "total_produtos": total_produtos,
        "total_categorias": total_categorias,
        "total_vendas": total_vendas,
        "sales_months": sales_months,
        "sales_totals": sales_totals,
        "product_labels": product_labels,
        "product_sales_totals": product_sales_totals,
        "daily_sales_dates": daily_sales_dates,
        "daily_sales_totals": daily_sales_totals,
        "category_labels": category_labels,
        "category_sales_totals": category_sales_totals,
        "stock_labels": stock_labels,
        "stock_totals": stock_totals,
        "total_stock": total_stock,
        "periodo": periodo,
    }

    return render(request, "store/index.html", context)


def cadastros(request):
    categorias = Categoria.objects.all()
    context = {"categorias": categorias}
    return render(request, "store/cadastros/cadastros.html", context)


def estoque(request):
    try:
        # Validação do Método HTTP
        if request.method != "GET":
            return JsonResponse({"error": "Método não permitido. Use GET."}, status=405)

        # Recuperação de todos os produtos do estoque
        estoque = Produto.objects.all()

        # Construção do contexto com detalhes dos produtos
        context = {
            "estoque": [
                {
                    "nome": p.nome,
                    "descricao": p.descricao,
                    "preco": p.preco,
                    "estoque_qntd": p.estoque_qntd,
                    "categoria": p.categoria.nome if p.categoria else "Sem categoria",
                }
                for p in estoque
            ]
        }

        # Verificação se o estoque está vazio
        if not context["estoque"]:
            return JsonResponse({"message": "Estoque vazio."}, status=404)

        # Renderização do template com o contexto
        return render(request, "store/estoque/estoque.html", context)

    except Exception as e:
        # Log do erro (pode-se usar um logger aqui)
        print(f"Erro ao buscar estoque: {e}")
        return JsonResponse(
            {"error": "Ocorreu um erro ao buscar o estoque."}, status=500
        )


def pdv(request):
    return render(request, "store/pdv/pdv.html")


def buscar_produtos_pdv(request):
    try:
        # Validação de entrada
        if not request.method == "POST":
            return JsonResponse(
                {"error": "Método não permitido. Use POST."}, status=405
            )

        nome = request.POST.get("buscaProdutoNome", "").strip()
        categoria = request.POST.get("buscaProdutoCategoria", "").strip()

        # Construção da query de forma segura
        Q_produtos = Q()
        if nome:
            Q_produtos &= Q(nome__icontains=nome)
        if categoria:
            Q_produtos &= Q(categoria__nome__icontains=categoria)

        # Filtragem dos produtos
        produtos = Produto.objects.filter(Q_produtos, estoque_disp=True)

        # Verificação se produtos foram encontrados
        if not produtos.exists():
            return JsonResponse({"message": "Nenhum produto encontrado."}, status=404)

        # Renderização do template com o contexto
        context = {"produtos": produtos}
        return render(request, "store/pdv/produtos_buscados.html", context)

    except Exception as e:
        # Log do erro (pode-se usar um logger aqui)
        return JsonResponse(
            {"error": "Ocorreu um erro ao buscar os produtos."}, status=500
        )


def vendas(request):
    vendas = (
        Vendas.objects.all()
        .prefetch_related("vendaproduto_set__produto")
        .order_by("-data_venda")
    )
    vendas_total = vendas.aggregate(total=Sum("total"))["total"].quantize(
        Decimal("0.01")
    )
    context = {"vendas": vendas, "vendas_total": vendas_total}
    return render(request, "store/vendas/vendas.html", context)
