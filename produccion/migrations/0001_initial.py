# Generated by Django 5.0.6 on 2024-07-07 19:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=3, unique=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=3, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.planta')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroProduccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('litros', models.PositiveIntegerField()),
                ('fecha', models.DateField()),
                ('turno', models.CharField(choices=[('AM', 'Mañana'), ('PM', 'Tarde'), ('MM', 'Noche')], max_length=2)),
                ('hora_registro', models.TimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(blank=True, null=True)),
                ('eliminado', models.BooleanField(default=False)),
                ('modificado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modificado_por', to=settings.AUTH_USER_MODEL)),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.producto')),
            ],
        ),
    ]
