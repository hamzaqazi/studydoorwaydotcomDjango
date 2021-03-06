# Generated by Django 3.1.3 on 2021-04-19 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('topic', models.CharField(max_length=120)),
                ('number_of_questions', models.IntegerField()),
                ('time', models.IntegerField(help_text='Duration of the quiz in minutes')),
                ('required_score_to_pass', models.IntegerField(help_text='Required score in %')),
                ('difficulty', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('class_room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.classroom')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Quizes',
            },
        ),
    ]
