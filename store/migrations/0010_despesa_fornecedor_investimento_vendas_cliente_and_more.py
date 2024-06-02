# Generated by Django 5.0.4 on 2024-06-02 07:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_vendas_produtos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateField()),
                ('categoria', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Despesa',
                'verbose_name_plural': 'Despesas',
                'db_table': 'tb_despesas',
                'ordering': ['data'],
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('contato', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('endereco', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'db_table': 'tb_fornecedores',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Investimento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateField()),
                ('descricao', models.TextField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Investimento',
                'verbose_name_plural': 'Investimentos',
                'db_table': 'tb_investimentos',
                'ordering': ['data'],
            },
        ),
        migrations.AddField(
            model_name='vendas',
            name='cliente',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.cliente'),
        ),
        migrations.CreateModel(
            name='MateriaPrima',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantidade_estoque', models.IntegerField()),
                ('fornecedor', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.fornecedor')),
            ],
            options={
                'verbose_name': 'Matéria Prima',
                'verbose_name_plural': 'Matérias Primas',
                'db_table': 'tb_materias_primas',
                'ordering': ['nome'],
            },
        ),
    ]