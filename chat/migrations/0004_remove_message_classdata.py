# Generated by Django 3.1.3 on 2021-04-10 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_classdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='classdata',
        ),
    ]