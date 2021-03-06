# Generated by Django 3.1.3 on 2021-06-24 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0003_auto_20210425_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True, max_length=3000)),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, '1 - Trash'), (2, '2 - Horrible'), (3, '3 - Terrible'), (4, '4 - Bad'), (5, '5 - OK'), (6, '6 - Understandable'), (7, '7 - Good'), (8, '8 - Very Good'), (9, '9 - Perfect'), (10, '10 - Master Piece')])),
                ('likes', models.PositiveIntegerField(default=0)),
                ('unlikes', models.PositiveIntegerField(default=0)),
                ('class_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.classroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
