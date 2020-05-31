# Generated by Django 2.2.12 on 2020-05-23 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_auto_20200523_1502"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]