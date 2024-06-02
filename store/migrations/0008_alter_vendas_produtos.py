# Generated by Django 5.0.4 on 2024-06-02 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_vendas_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendas',
            name='produtos',
            field=models.ManyToManyField(related_name='vendas_produtos', through='store.VendaProduto', to='store.produto'),
        ),
    ]