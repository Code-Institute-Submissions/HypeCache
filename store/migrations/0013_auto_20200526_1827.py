# Generated by Django 2.2.12 on 2020-05-26 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20200526_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('lower', 'Bottoms'), ('tops', 'Tops'), ('outerwear', 'Outerwear'), ('shoes', 'Shoes'), ('misc', 'Accessories and Misc')], max_length=10, null=True),
        ),
    ]
