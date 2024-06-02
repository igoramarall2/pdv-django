from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vendas, VendaProduto, Produto
from django.db import transaction
import json
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import os

@csrf_exempt
@transaction.atomic
def finalizar_compra(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        carrinho = data.get('carrinho', [])
        total = data.get('total', 0)

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
        # Atualizar o estoque
        for item in carrinho:
            produto = Produto.objects.get(nome=item['name'])
            quantidade = item['quantity']
            produto.estoque_qntd -= quantidade
            produto.save()
        # Marcar como False caso o estoque seja 0
        for item in carrinho:
            produto = Produto.objects.get(nome=item['name'])
            if produto.estoque_qntd == 0:
                produto.estoque_disp = False
                produto.save()

        # Gerar nota fiscal
        nota_fiscal_path = gerar_nota_fiscal(venda)

        return JsonResponse({'message': 'Compra finalizada com sucesso.', 'nota_fiscal_url': nota_fiscal_path})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

def gerar_nota_fiscal(venda):
    # Diretório onde o PDF será salvo
    notas_fiscais_dir = os.path.join(settings.MEDIA_ROOT, 'notas_fiscais')

    # Criar o diretório se ele não existir
    os.makedirs(notas_fiscais_dir, exist_ok=True)

    # Caminho do arquivo PDF
    pdf_path = os.path.join(notas_fiscais_dir, f'venda_{venda.id}.pdf')

    # Configurar o documento PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Estilo do parágrafo
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    # Data da venda
    # data_paragraph = Paragraph(f"Data: {timezone.now().strftime('%d/%m/%Y')}", styleN)
    # elements.append(data_paragraph)

    # Dados da nota fiscal
    data = [
        ['Nota Fiscal', f'Venda #{venda.id}'],
        ['Nome do Produto', 'Quantidade', 'Preço Unitário', 'Subtotal']
    ]

    for item in venda.vendaproduto_set.all():
        data.append([
            item.produto.nome,
            item.quantidade,
            f'R${item.produto.preco:.2f}',
            f'R${item.subtotal:.2f}'
        ])

    # Adiciona a linha de total no final
    data.append(['', f"Data: {timezone.now().strftime('%d/%m/%Y')}", 'Total', f'R${venda.total:.2f}'])

    # Criar a tabela
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    elements.append(table)
    doc.build(elements)

    # Retornar o caminho do PDF
    return os.path.join(settings.MEDIA_URL, f'notas_fiscais/venda_{venda.id}.pdf')