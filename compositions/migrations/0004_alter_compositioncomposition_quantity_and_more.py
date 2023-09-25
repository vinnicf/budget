# Generated by Django 4.0.4 on 2023-09-25 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0003_alter_compositioncomposition_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compositioncomposition',
            name='quantity',
            field=models.DecimalField(decimal_places=10, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='compositioninsumo',
            name='quantity',
            field=models.DecimalField(decimal_places=10, max_digits=25, null=True),
        ),
    ]
