# Generated by Django 2.2.12 on 2020-05-29 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0016_auto_20200528_1409"),
    ]

    operations = [
        migrations.AddField(
            model_name="shippingaddress",
            name="first_name",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="shippingaddress",
            name="last_name",
            field=models.CharField(max_length=200, null=True),
        ),
    ]