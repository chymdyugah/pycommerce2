# Generated by Django 2.2.2 on 2020-09-16 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irish', '0008_shipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
