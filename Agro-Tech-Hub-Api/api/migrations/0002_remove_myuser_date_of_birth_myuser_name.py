# Generated by Django 5.0.6 on 2024-06-07 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='myuser',
            name='name',
            field=models.TextField(default='Guest'),
        ),
    ]