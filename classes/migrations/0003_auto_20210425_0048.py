# Generated by Django 3.1.3 on 2021-04-24 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_auto_20210421_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='created_at',
            field=models.DateField(),
        ),
    ]