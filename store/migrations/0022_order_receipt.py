# Generated by Django 2.2.12 on 2020-05-30 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0021_auto_20200530_0050"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="receipt",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
