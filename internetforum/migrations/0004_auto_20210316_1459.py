# Generated by Django 3.1.3 on 2021-03-16 09:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internetforum', '0003_auto_20210312_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='detail',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
