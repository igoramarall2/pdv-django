from django.shortcuts import render, redirect
from .models import (
    Cliente,
    Fornecedor,
    Produto,
    Categoria,
    Vendas,
    VendaProduto,
    MateriaPrima,
)
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from django.utils import timezone
import json
from datetime import timedelta
from decimal import Decimal
from .forms import FornecedorForm


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def get_inicio_periodo(periodo, agora):
    """Retorna o início do período baseado no período selecionado."""
    periodos = {
        "Hoje": 1,
        "7 dias": 7,
        "15 dias": 15,
        "30 dias": 30,
        "90 dias": 90,
        "180 dias": 180,
        "365 dias": 365,
    }
    return agora - timedelta(days=periodos.get(periodo, 1))


def get_sales_data(vendas_filtradas):
    """Retorna dados de vendas para gráficos."""
    sales_data = (
        vendas_filtradas.extra(select={"month": 'strftime("%%m", data_venda)'})
        .values("month")
        .annotate(total=Sum("total"))
        .order_by("month")
    )
    return json.dumps(
        [item["month"] for item in sales_data], cls=DecimalEncoder
    ), json.dumps([item["total"] for item in sales_data], cls=DecimalEncoder)


def get_product_sales_data(vendas_filtradas):
    """Retorna dados de vendas por produto."""
    product_sales_data = (
        VendaProduto.objects.filter(venda__in=vendas_filtradas)
        .values("produto__nome")
        .annotate(total=Sum("quantidade"))
        .order_by("produto__nome")
    )
    return json.dumps(
        [f"{item['produto__nome'][:12]}..." for item in product_sales_data]
    ), json.dumps([item["total"] for item in product_sales_data], cls=DecimalEncoder)


def get_daily_sales_data(vendas_filtradas):
    """Retorna dados de vendas diárias."""
    daily_sales_data = (
        vendas_filtradas.extra(select={"day": 'strftime("%%Y-%%m-%%d", data_venda)'})
        .values("day")
        .annotate(total=Sum("total"))
        .order_by("day")
    )
    return json.dumps(
        [item["day"] for item in daily_sales_data], cls=DecimalEncoder
    ), json.dumps([item["total"] for item in daily_sales_data], cls=DecimalEncoder)


def get_category_sales_data(vendas_filtradas):
    """Retorna dados de vendas por categoria."""
    category_sales_data = (
        VendaProduto.objects.filter(venda__in=vendas_filtradas)
        .values("produto__categoria__nome")
        .annotate(total=Sum("quantidade"))
        .order_by("produto__categoria__nome")
    )
    return json.dumps(
        [item["produto__categoria__nome"] for item in category_sales_data]
    ), json.dumps([item["total"] for item in category_sales_data], cls=DecimalEncoder)


def get_stock_data():
    """Retorna dados de estoque por categoria."""
    stock_data = (
        Produto.objects.values("categoria__nome")
        .annotate(total_stock=Sum("estoque_qntd"))
        .order_by("categoria__nome")
    )
    return json.dumps([item["categoria__nome"] for item in stock_data]), json.dumps(
        [item["total_stock"] for item in stock_data], cls=DecimalEncoder
    )


def index(request):
    """View principal do painel, exibe dados consolidados."""
    total_produtos = Produto.objects.count()
    total_categorias = Categoria.objects.count()
    total_vendas = Vendas.objects.count()
    periodo = request.GET.get("periodo", "Hoje")
    agora = timezone.now()

    inicio_periodo = get_inicio_periodo(periodo, agora)
    vendas_filtradas = Vendas.objects.filter(data_venda__gte=inicio_periodo)

    sales_months, sales_totals = get_sales_data(vendas_filtradas)
    product_labels, product_sales_totals = get_product_sales_data(vendas_filtradas)
    daily_sales_dates, daily_sales_totals = get_daily_sales_data(vendas_filtradas)
    category_labels, category_sales_totals = get_category_sales_data(vendas_filtradas)
    stock_labels, stock_totals = get_stock_data()

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
    """View para exibir e gerenciar cadastros de categorias e fornecedores."""
    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.all()
    context = {"categorias": categorias, "fornecedores": fornecedores}
    return render(request, "store/cadastros/cadastros.html", context)


def estoque(request):
    """View para exibir o estoque de produtos."""
    try:
        if request.method != "GET":
            return JsonResponse({"error": "Método não permitido. Use GET."}, status=405)

        estoque = Produto.objects.all()

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

        if not context["estoque"]:
            return JsonResponse({"message": "Estoque vazio."}, status=404)

        return render(request, "store/estoque/estoque.html", context)

    except Exception as e:
        print(f"Erro ao buscar estoque: {e}")
        return JsonResponse(
            {"error": "Ocorreu um erro ao buscar o estoque."}, status=500
        )


def pdv(request):
    """View para o ponto de venda."""
    return render(request, "store/pdv/pdv.html")


def buscar_produtos_pdv(request):
    """Busca produtos para o ponto de venda."""
    try:
        if request.method != "POST":
            return JsonResponse(
                {"error": "Método não permitido. Use POST."}, status=405
            )

        nome = request.POST.get("buscaProdutoNome", "").strip()
        categoria = request.POST.get("buscaProdutoCategoria", "").strip()

        Q_produtos = Q()
        if nome:
            Q_produtos &= Q(nome__icontains=nome)
        if categoria:
            Q_produtos &= Q(categoria__nome__icontains=categoria)

        produtos = Produto.objects.filter(Q_produtos, estoque_disp=True)

        if not produtos.exists():
            return JsonResponse({"message": "Nenhum produto encontrado."}, status=404)

        context = {"produtos": produtos}
        return render(request, "store/pdv/produtos_buscados.html", context)

    except Exception as e:
        return JsonResponse(
            {"error": "Ocorreu um erro ao buscar os produtos."}, status=500
        )


def vendas(request):
    """View para exibir todas as vendas realizadas."""
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


def fornecedores(request):
    """View para exibir os fornecedores."""
    fornecedores = Fornecedor.objects.all()
    context = {"fornecedores": fornecedores}
    return render(request, "store/fornecedores/fornecedores.html", context)


def materias_primas(request):
    """View para exibir as matérias-primas."""
    materias_primas = MateriaPrima.objects.all()
    context = {"materias_primas": materias_primas}
    return render(request, "store/materias_primas/materias_primas.html", context)


def despesas(request):
    """View para exibir as despesas."""
    return render(request, "store/despesas/despesas.html")


def investimentos(request):
    """View para exibir os investimentos."""
    return render(request, "store/investimentos/investimentos.html")
