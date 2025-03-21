# Generated by Django 5.1.6 on 2025-02-06 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Category Name'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Product Name')),
                ('description', models.TextField(default='The description is not available yet')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Product Price')),
                ('size', models.IntegerField(default=50, verbose_name='Product Size')),
                ('color', models.CharField(max_length=30, verbose_name='Product Color')),
                ('quantity', models.IntegerField(default=0, verbose_name='Product Quantity')),
                ('brand', models.TextField(default='The brand is not available')),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category', verbose_name='Product Category')),
            ],
        ),
    ]
