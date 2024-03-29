# Generated by Django 5.0.2 on 2024-02-18 16:46

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=64)),
                ('category', models.CharField(choices=[('pol', 'Politics'), ('art', 'Art'), ('tech', 'Tech'), ('trivia', 'Trivia')], max_length=8)),
                ('region', models.CharField(choices=[('uk', 'United Kingdom'), ('eu', 'Europe'), ('w', 'World')], max_length=8)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('details', models.CharField(max_length=128)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
