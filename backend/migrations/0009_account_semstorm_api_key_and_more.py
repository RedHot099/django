# Generated by Django 4.2.4 on 2023-11-14 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_account_tokens_used_alter_zaplecze_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='semstorm_api_key',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='account',
            name='openai_api_key',
            field=models.CharField(default='', max_length=64),
        ),
    ]
