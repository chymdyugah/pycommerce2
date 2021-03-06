# Generated by Django 2.2.2 on 2020-09-17 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('irish', '0009_cart_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='null', upload_to=''),
        ),
    ]
