# Generated by Django 2.2.2 on 2020-09-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irish', '0013_product_prodid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prodid',
            field=models.CharField(default='prod0', max_length=255),
        ),
    ]
