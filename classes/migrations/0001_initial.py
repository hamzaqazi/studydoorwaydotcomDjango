# Generated by Django 3.1.3 on 2021-04-19 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement_text', models.TextField(max_length=500)),
                ('announcement_file', models.FileField(blank=True, upload_to='files/announcement_file/')),
                ('announcement_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('instruction', models.TextField(blank=True, max_length=500, null=True)),
                ('file', models.FileField(blank=True, upload_to='files/t_assignments/')),
                ('points', models.CharField(choices=[('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'), ('60', '60'), ('70', '70'), ('80', '80'), ('90', '90'), ('100', '100')], default=100, max_length=100, null=True)),
                ('due_date', models.DateTimeField()),
                ('assigning_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_key', models.CharField(max_length=50, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('class_name', models.CharField(max_length=250)),
                ('section', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=200, null=True)),
                ('subject', models.CharField(max_length=250, null=True)),
                ('title_image', models.ImageField(blank=True, default='classTitle image.jpg', null=True, upload_to='classTitleImages/')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/s_submissions/')),
                ('submitted_at', models.DateTimeField(auto_now=True)),
                ('last_updated', models.DateTimeField(null=True)),
                ('grade', models.CharField(blank=True, default='No grade yet', max_length=100, null=True)),
                ('feedback', models.CharField(blank=True, default='No feedback yet', max_length=100, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='classes.assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('notification_date', models.DateField(auto_now_add=True)),
                ('viewed', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.assignment')),
                ('class_room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.classroom')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.classroom')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=255)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='classes.announcement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField(default=False)),
                ('absent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('class_room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='classes.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='classes.student')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='class_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.classroom'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='announcement',
            name='class_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='classes.classroom'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='likes',
            field=models.ManyToManyField(related_name='announcement_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='announcement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
