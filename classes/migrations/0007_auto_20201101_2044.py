# Generated by Django 3.1.1 on 2020-11-01 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_classroom_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='class_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.classroom'),
        ),
        migrations.DeleteModel(
            name='ClassInfo',
        ),
    ]
