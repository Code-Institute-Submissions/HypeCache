# Generated by Django 2.2.12 on 2020-05-23 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_product_date_posted"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="product_pics"),
        ),
    ]