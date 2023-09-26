# Generated by Django 4.0.4 on 2023-09-25 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0002_state_remove_insumo_cost_composition_codigo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compositioncomposition',
            name='quantity',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='compositioninsumo',
            name='quantity',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
    ]