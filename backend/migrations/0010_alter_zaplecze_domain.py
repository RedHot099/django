# Generated by Django 4.2.4 on 2023-11-20 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_account_semstorm_api_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zaplecze',
            name='domain',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
