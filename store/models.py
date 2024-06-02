from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]
        db_table = "tb_clientes"


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]
        db_table = "tb_categoria"


class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_qntd = models.IntegerField()
    estoque_disp = models.BooleanField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]
        db_table = "tb_produtos"


class Vendas(models.Model):
    id = models.AutoField(primary_key=True)
    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    produtos = models.ManyToManyField(
        Produto, through="VendaProduto", related_name="vendasprodutos"
    )

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ["data_venda"]
        db_table = "tb_vendas"


class VendaProduto(models.Model):
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    venda = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.produto.nome

    class Meta:
        verbose_name = "VendaProduto"
        verbose_name_plural = "VendaProdutos"
        ordering = ["produto"]
        db_table = "tb_venda_produto"


# Novas tabelas
class Fornecedor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    contato = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ["nome"]
        db_table = "tb_fornecedores"


class MateriaPrima(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.IntegerField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Matéria Prima"
        verbose_name_plural = "Matérias Primas"
        ordering = ["nome"]
        db_table = "tb_materias_primas"


class Despesa(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    categoria = models.CharField(max_length=100)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.categoria} - {self.valor}"

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"
        ordering = ["data"]
        db_table = "tb_despesas"


class Investimento(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tipo} - {self.valor}"

    class Meta:
        verbose_name = "Investimento"
        verbose_name_plural = "Investimentos"
        ordering = ["data"]
        db_table = "tb_investimentos"


# Novas tabelas


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(
        max_length=50,
        choices=[("admin", "Admin"), ("caixa", "Caixa"), ("gerente", "Gerente")],
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo}"

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuário"
        ordering = ["usuario"]
        db_table = "tb_perfis_usuarios"


class MetodoPagamento(models.Model):
    id = models.AutoField(primary_key=True)
    metodo = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.metodo

    class Meta:
        verbose_name = "Método de Pagamento"
        verbose_name_plural = "Métodos de Pagamento"
        ordering = ["metodo"]
        db_table = "tb_metodos_pagamento"


class TransacaoPagamento(models.Model):
    id = models.AutoField(primary_key=True)
    venda = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    metodo_pagamento = models.ForeignKey(MetodoPagamento, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_transacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.venda.id} - {self.metodo_pagamento.metodo} - {self.valor}"

    class Meta:
        verbose_name = "Transação de Pagamento"
        verbose_name_plural = "Transações de Pagamento"
        ordering = ["data_transacao"]
        db_table = "tb_transacoes_pagamento"


class MovimentacaoEstoque(models.Model):
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    tipo_movimentacao = models.CharField(
        max_length=50,
        choices=[("entrada", "Entrada"), ("saida", "Saída"), ("ajuste", "Ajuste")],
    )
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo_movimentacao} - {self.quantidade}"

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ["data"]
        db_table = "tb_movimentacoes_estoque"


class RelatorioVendas(models.Model):
    id = models.AutoField(primary_key=True)
    data_relatorio = models.DateField()
    total_vendas = models.DecimalField(max_digits=10, decimal_places=2)
    total_itens_vendidos = models.IntegerField()
    relatorio_gerado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Relatório {self.id} - {self.data_relatorio}"

    class Meta:
        verbose_name = "Relatório de Vendas"
        verbose_name_plural = "Relatórios de Vendas"
        ordering = ["-data_relatorio"]
        db_table = "tb_relatorios_vendas"


class LogAcao(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.acao} - {self.timestamp}"

    class Meta:
        verbose_name = "Log de Ação"
        verbose_name_plural = "Logs de Ação"
        ordering = ["-timestamp"]
        db_table = "tb_logs_acoes"


class Promocao(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    desconto_percentual = models.DecimalField(max_digits=5, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Promoção"
        verbose_name_plural = "Promoções"
        ordering = ["-data_inicio"]
        db_table = "tb_promocoes"


class AplicacaoPromocao(models.Model):
    id = models.AutoField(primary_key=True)
    venda = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    promocao = models.ForeignKey(Promocao, on_delete=models.CASCADE)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2)
    aplicado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.venda.id} - {self.promocao.nome} - {self.valor_desconto}"

    class Meta:
        verbose_name = "Aplicação de Promoção"
        verbose_name_plural = "Aplicações de Promoção"
        ordering = ["aplicado_em"]
        db_table = "tb_aplicacoes_promocao"
