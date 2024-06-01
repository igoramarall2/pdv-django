from django.contrib import admin
from .models import Cliente, Categoria, Produto
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Produto)

