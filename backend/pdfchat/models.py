from django.db import models

# Create your models here.
class File_Details(models.Model):
    _id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.file_name