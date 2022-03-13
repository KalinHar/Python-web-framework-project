# Generated by Django 4.0.3 on 2022-03-03 07:53

import course_project.web.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField()),
                ('taxes', models.JSONField()),
            ],
            options={
                'ordering': ('-from_date',),
            },
        ),
        migrations.CreateModel(
            name='OldDebts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(auto_now_add=True)),
                ('debts', models.FloatField()),
                ('indications', models.CharField(max_length=40)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.client')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=300)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/notice_images/', validators=[course_project.web.models.file_max_size])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-from_date',),
            },
        ),
    ]
