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

# # Create your models here.
# class File_Details(models.Model):
#     _id = models.UUIDField(primary_key=True, editable=False)
#     file_name = models.CharField(max_length=255)
#     file = models.FileField(upload_to='files/')
#     # thread_id = models.CharField(max_length=255)
#     # title = models.CharField(max_length=255)

#     def __str__(self):
#         return self.file_name
    
# class Conversation(models.Model):
#     chat_id = models.CharField(max_length=255)  # Add this field
#     role = models.CharField(max_length=50)
#     content = models.TextField()

#     def __str__(self):
#         return f"{self.role}: {self.content}"