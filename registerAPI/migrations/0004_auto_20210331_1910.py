# Generated by Django 3.0.4 on 2021-03-31 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registerAPI', '0003_auto_20210327_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=30),
        ),
    ]