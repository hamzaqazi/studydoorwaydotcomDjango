# Generated by Django 3.1.3 on 2021-02-19 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_announcement'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='class_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.classroom'),
        ),
    ]