from django.db import models
import uuid


class Chat_Details(models.Model):
    _id = models.UUIDField(primary_key=True, editable=False)
    file_name = models.CharField(max_length=255)
    thread_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    openai_file_id=models.CharField(max_length=255,default='fileid')
    assistant_id=models.CharField(max_length=255,default='assistantid')
    def __str__(self):
        return self.file_name
