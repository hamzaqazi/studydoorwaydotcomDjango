# Generated by Django 3.1.1 on 2020-10-30 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_auto_20201030_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
