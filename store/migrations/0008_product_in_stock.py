# Generated by Django 2.2.12 on 2020-05-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_product_colour"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="in_stock",
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
