# Generated by Django 3.1.3 on 2021-04-21 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]