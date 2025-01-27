# Generated by Django 5.0.6 on 2024-09-04 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_remove_message_chat_room_remove_message_sender_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmodel',
            old_name='room_group_name',
            new_name='room_name',
        ),
        migrations.AlterUniqueTogether(
            name='chatmodel',
            unique_together={('name', 'receiver', 'room_name')},
        ),
    ]
