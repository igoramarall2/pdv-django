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
        ordering = ["nome"]  # Order authors by name
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
        ordering = ["nome"]  # Order authors by name
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
        ordering = ["nome"]  # Order authors by name
        db_table = "tb_produtos"
        
class Vendas(models.Model):
    id = models.AutoField(primary_key=True)
    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    produtos = models.ManyToManyField(Produto, through='VendaProduto')
    
    def __str__(self):
        return self.cliente.nome
    
    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ["data_venda"]  # Order authors by name
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
        ordering = ["produto"]  # Order authors by name
        db_table = "tb_venda_produto"

