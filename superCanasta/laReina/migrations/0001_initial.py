# Generated by Django 5.0.6 on 2024-10-23 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('supermercado', models.CharField(max_length=255)),
                ('categoria', models.CharField(max_length=255)),
                ('fecha_act', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]