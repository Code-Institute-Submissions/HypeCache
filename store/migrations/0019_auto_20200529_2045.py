# Generated by Django 2.2.12 on 2020-05-29 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0018_auto_20200529_1855"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
