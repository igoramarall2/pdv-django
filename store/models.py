from django.db import models


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
