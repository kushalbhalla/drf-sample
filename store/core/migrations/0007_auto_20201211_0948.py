# Generated by Django 3.0.5 on 2020-12-11 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20201211_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeinfo',
            name='product_quantity',
            field=models.IntegerField(),
        ),
    ]