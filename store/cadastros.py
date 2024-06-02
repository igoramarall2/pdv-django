from django.http import JsonResponse
from django.db import transaction
from store.models import Categoria, Cliente, Produto, Fornecedor, MateriaPrima


@transaction.atomic
def cadastros_clientes(request):
    campos_cliente = {
        "nomeCli": "nome",
        "cpfCli": "cpf",
        "telefoneCli": "telefone",
        "enderecoCli": "endereco",
        "estadoCli": "estado",
        "cepCli": "cep",
        "cidadeCli": "cidade",
        "emailCli": "email",
    }
    cadastros_clientes = Cliente()

    for campo_formulario, atributo_cliente in campos_cliente.items():
        valor = request.POST.get(campo_formulario)
        setattr(cadastros_clientes, atributo_cliente, valor)

    cadastros_clientes.save()

    if cadastros_clientes.id:
        return JsonResponse({"message": "Cadastro com Sucesso"})


@transaction.atomic
def cadastro_categorias(request):
    campos_categoria = {
        "nomeCat": "nome",
        "desCat": "descricao",
    }
    cadastros_categorias = Categoria()

    for campo_formulario, atributo_categoria in campos_categoria.items():
        valor = request.POST.get(campo_formulario)
        setattr(cadastros_categorias, atributo_categoria, valor)

    cadastros_categorias.save()

    if cadastros_categorias.id:
        return JsonResponse({"message": "Cadastro com Sucesso"})


@transaction.atomic
def cadastro_produtos(request):
    campos_produto = {
        "nomeProd": "nome",
        "desProd": "descricao",
        "preProd": "preco",
        "qntProd": "estoque_qntd",
    }
    cadastros_produtos = Produto()

    for campo_formulario, atributo_produto in campos_produto.items():
        valor = request.POST.get(campo_formulario)
        setattr(cadastros_produtos, atributo_produto, valor)

    cadastros_produtos.categoria_id = Categoria.objects.get(
        id=request.POST.get("catProd")
    ).id
    cadastros_produtos.save()

    if cadastros_produtos.id:
        return JsonResponse({"message": "Cadastro com Sucesso"})


@transaction.atomic
def cadastro_fornecedores(request):
    campos_fornecedor = {
        "nomeFor": "nome",
        "contatoFor": "contato",
        "telefoneFor": "telefone",
        "emailFor": "email",
        "enderecoFor": "endereco",
    }
    cadastros_fornecedores = Fornecedor()

    for campo_formulario, atributo_fornecedor in campos_fornecedor.items():
        valor = request.POST.get(campo_formulario)
        setattr(cadastros_fornecedores, atributo_fornecedor, valor)

    cadastros_fornecedores.save()

    if cadastros_fornecedores.id:
        return JsonResponse({"message": "Cadastro com Sucesso"})


@transaction.atomic
def cadastro_materia_prima(request):
    campos_materia_prima = {
        "nomeMat": "nome",
        "descricaoMat": "descricao",
        "precoUnitarioMat": "preco_unitario",
        "quantidadeEstoqueMat": "quantidade_estoque",
    }
    cadastros_materia_prima = MateriaPrima()

    for campo_formulario, atributo_materia_prima in campos_materia_prima.items():
        valor = request.POST.get(campo_formulario)
        setattr(cadastros_materia_prima, atributo_materia_prima, valor)

    cadastros_materia_prima.fornecedor_id = Fornecedor.objects.get(
        id=request.POST.get("fornecedorMat")
    ).id
    cadastros_materia_prima.save()

    if cadastros_materia_prima.id:
        return JsonResponse({"message": "Cadastro com Sucesso"})
