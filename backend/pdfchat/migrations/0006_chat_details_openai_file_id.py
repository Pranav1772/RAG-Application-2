# Generated by Django 5.0.3 on 2024-03-11 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfchat', '0005_chat_details_delete_conversation_delete_file_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat_details',
            name='openai_file_id',
            field=models.CharField(default='your_default_value', max_length=255),
        ),
    ]
