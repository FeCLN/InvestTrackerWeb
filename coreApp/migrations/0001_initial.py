# Generated by Django 5.1 on 2024-08-21 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('email', models.TextField(max_length=255)),
                ('password', models.TextField(max_length=255)),
            ],
        ),
    ]