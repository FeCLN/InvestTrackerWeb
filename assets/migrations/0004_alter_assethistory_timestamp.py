# Generated by Django 5.0.8 on 2024-08-22 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_assethistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assethistory',
            name='timestamp',
            field=models.TextField(null=True),
        ),
    ]
