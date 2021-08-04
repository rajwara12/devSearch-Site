# Generated by Django 3.2.3 on 2021-08-03 07:42

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
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=90)),
                ('short_intro', models.TextField()),
                ('bio', models.TextField()),
                ('prof_img', models.ImageField(upload_to='images')),
                ('social_links_git', models.CharField(max_length=200)),
                ('skills', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=500)),
                ('project_desc', models.TextField()),
                ('project_img', models.ImageField(upload_to='images')),
                ('project_link', models.CharField(max_length=1000)),
                ('myaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.useraccount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
